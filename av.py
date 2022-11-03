import openai
import pyttsx3
import speech_recognition as sr

#api-key
openai.api_key = "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"

#setmic
mic = sr.Microphone(device_index=1)

#input
user_name=input("Escribe tu nombre: ")
print("Tu nombre es: "+user_name)
ia_name=input("Escribe el nombre de la IA: \n*")
print("La IA se llama: "+ia_name)
context= "Joy es una asistente virtual muy sarcástica y siempre hace bromas"
#input("Describe a tu IA: ")

#start
conversation = ""
engine= pyttsx3.init()
listener = sr.Recognizer()

#sr properties
listener.energy_threshold=100
listener.dynamic_energy_threshold = False
    #sr voice properties
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[2].id)
#for voice in voices:
#    print (voice, voice.id)

def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    with mic as source:
        print("(("+ia_name+" está escuchando))")
        listener.adjust_for_ambient_noise(source, duration= 0.2)
        voice = listener.listen(source)

    print("(("+ia_name+" dejó de escuchar))")

    try:
        rec = listener.recognize_google(voice, language= "es-ES")
        rec = rec.replace(ia_name, "")
    except:
        pass
    return rec


def run():
    rec = listen()
    if "reproduce" in rec:
        music = rec.replace("reproduce","")
        talk("Reproduciendo " + music)

while True:
    run()