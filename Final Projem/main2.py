import google.generativeai as genai
import api

genai.configure(api_key=api.api)

model = genai.GenerativeModel('gemini-pro')

def geminiai(mesaj):
    if not mesaj:
        return "Error: The message is empty."
    response = model.generate_content(str(mesaj))
    for chunk in response:
        with open("output.txt", "a", encoding="UTF-8") as f:
            f.write(chunk.text)
    return chunk.text
             
def c(mesaj):
    return geminiai(mesaj)

if __name__=="__main__":
    while True:
        mesaj2 = input("Soru sor\n")
        print(c(mesaj2))