import speech_recognition


def ing_konusma():
    mikrofon=speech_recognition.Microphone()
    kayıt=speech_recognition.Recognizer()

    with mikrofon as s_d:
        kayıt.adjust_for_ambient_noise(s_d)
        ses=kayıt.listen(s_d)
        try:
            return kayıt.recognize_google(ses,language="en-GB")
        except:
            return "Konuşmanız algılanamadı."
def tr_konusma():
    mikrofon=speech_recognition.Microphone()
    kayıt=speech_recognition.Recognizer()

    with mikrofon as s_d:
        kayıt.adjust_for_ambient_noise(s_d)
        ses=kayıt.listen(s_d)
        try:
            return kayıt.recognize_google(ses,language="tr-TR")
        except:
            return "Konuşmanız algılanamadı."





if __name__=="__main__":
    print("Lütfen konuşmaya başlayın.")
    x=tr_konusma()
    print(x)

    
