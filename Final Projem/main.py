# Import
from flask import Flask, render_template,request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import k
import main2
import requests
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from wordcloud import WordCloud
from matplotlib import pyplot as plt
app = Flask(__name__)
# SQLite'ı bağlama
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
class List_need(db.Model):
    saat=db.Column(db.String(100))
    content=db.Column(db.String(100))
    complete=db.Column(db.Boolean)
    id=db.Column(db.Integer,primary_key=True)

     
     
     
# İçerik sayfasını çalıştırma
@app.route('/')
def index():
    return render_template('index.html')


h_d_k={
    "Clouds":"Bulutlu",
    "Snow" : "Karlı",
    "Rain" :"Yağmurlu",
    "Mist" : "Sisli",
    "Clear" : "Açık hava" ,
    "Drizzle" : "Hafif yağmur",
    "Thunderstorm" : "Gökgürültülü fırtına",
    "Fog" : "Sisli"
}
api_key = "ff4d0f71153fc14f03f0ef1410af08a9"




def hava_f(sehir):
    if hava(sehir)[0]=="Bulutlu":
            return '6.png'
             

    elif hava(sehir)[0]=="Karlı":
            return '4.png'
             

    elif hava(sehir)[0]=="Sisli":
            return '3.png'
            
        
    elif hava(sehir)[0]=="Açık hava":
            return '2.png'
            
            
    elif hava(sehir)[0]=="Yağmurlu":
            return '5.png'
             
        
    elif hava(sehir)[0]=="Hafif yağmur":
            return '7.png'
            
        
    elif hava(sehir)[0]=="Gökgürültülü fırtına":
            return '1.png' 

                

def hava(sehir):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    if data["weather"][0]["main"] in h_d_k:
        return h_d_k[data["weather"][0]["main"]],data["main"]["temp"],data["wind"]["speed"],data["main"]["humidity"],data["main"]["pressure"],data["clouds"]["all"]
    else:
        return data["weather"][0]["main"],data["main"]["temp"],data["wind"]["speed"],data["main"]["humidity"],data["main"]["pressure"],data["clouds"]["all"]


@app.route("/y_l", methods=["POST"])
def y_l():
    content=request.form.get("icerik")
    saat=request.form.get("saat")
    d=List_need(content=content, saat=saat, complete=False)
    db.session.add(d)
    db.session.commit()
    return redirect(url_for("todo"))

@app.route("/h_d",methods=["GET","POST"])
def h_d():
    if request.method=="POST":
        sehir=request.form.get("sehir") 
        
        return render_template("v_g.html",
                h_d=hava(sehir)[0],
                d=hava(sehir)[1],
                r_h=hava(sehir)[2],
                n=hava(sehir)[3],
                b=hava(sehir)[4],
                b_s=hava(sehir)[5],
                h_f=hava_f(sehir)

                )
    else:
          return render_template("s_s.html")


@app.route("/complete/<id>")
def coplete(id):
    degisken=List_need.query.filter_by(id=id).first()
    degisken.complete=True
    db.session.commit()
    return redirect(url_for("todo"))

@app.route("/todo")
def todo():
    t_d=List_need.query.all()
    return render_template("todo.html",t_d=t_d)



@app.route('/cevap', methods=["POST"])
def cevap():
    c_m=request.form.get("subtitle")
    c2=main2.c(c_m)
    
    return render_template("s_a.html", c2=c2)

@app.route('/ozet', methods=["GET","POST"])
def ozet(sentences=2):
    if request.method=="POST":
        text=request.form.get("metin")



        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        sentences = sent_tokenize(text, language='turkish')
        stop_words = set(stopwords.words('turkish'))
        words = word_tokenize(text)
        words = [word.lower() for word in words if word.isalpha()]
        words = [word for word in words if word not in stop_words]
        lemmatizer = WordNetLemmatizer()

        words = [lemmatizer.lemmatize(word) for word in words]
        freq_dist = FreqDist(words)
        sentence_scores = {}

        for i, sentence in enumerate(sentences):
            sentence_words = word_tokenize(sentence.lower())
            sentence_score = sum([freq_dist[word] for word in sentence_words if word in freq_dist])

            sentence_scores[i] = sentence_score
        sorted_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
        selected_sentences = sorted_scores[:1]
        selected_sentences = sorted(selected_sentences)

        # Özet oluşturma
        summary = ' '.join([sentences[i] for i, _ in selected_sentences])
        return render_template("ozet.html", summary=summary)
        # Dinamik beceriler
    else:
         return render_template("ozet.html")
    

@app.route('/', methods=['POST'])
def process_form():
    button_chat = request.form.get('button_chat')
    button_hd = request.form.get('button_hd')
    button_o = request.form.get('button_o')
    button_todo = request.form.get('button_todo')
    return render_template('index.html', button_chat=button_chat, button_hd=button_hd, button_o=button_o, button_todo=button_todo)

    
@app.route('/ses')
def ses():
    s=k.tr_konusma()
    return render_template("s_a.html", s=s)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
