import openai
import pyttsx3
import speech_recognition as sr

#api-key
openai.api_key = "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"

#setMic
#for index, name in enumerate(sr.Microphone.list_microphone_names()):
#    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
mic = sr.Microphone(device_index=1)

#input
user_name=input("Escribe tu nombre: ")
ia_name=input("Escribe el nombre de la IA: ")
context= ia_name+" es una asistente virtual muy sarcástica y bromista aun asi servicial a "+user_name
#input("Describe a tu IA: ")

#start
engine= pyttsx3.init()
listener = sr.Recognizer()
text = ""
isListening = False

#sr properties
listener.energy_threshold=100
listener.dynamic_energy_threshold = False
    #sr voice properties
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[2].id)
#for voice in voices:
#    print (voice, voice.id)



def gpt3(text):
    #using GPT3
    conversation = ""
    print(user_name+": "+text)
    conversation += "\n"+user_name+": " + text + "\n"+ia_name+":"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=(context+"\n\n"+conversation),
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " "+user_name+":", " "+ia_name+":"]	
    )
    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str = response_str.split(user_name + ": ", 1)[0].split(ia_name + ": ", 1)[0]
    conversation += response_str + "\n"
    print(ia_name+": "+response_str)
    return response_str

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with mic as source:
        listener.adjust_for_ambient_noise(source, duration= 0.2)
        voice = listener.listen(source)

    if isListening == False:
        print("(("+ia_name+" no está escuchando))")
    else:
        print("(("+ia_name+" está escuchando))")

    try:
        rec = listener.recognize_google(voice, language= "es-ES")
    except LookupError:
        print(ia_name+": No te entendí\n")
        engine.say(ia_name+": No te entendí")
    except Exception:
        print("((Esperando))")
        return ""
    return rec

while True:
    text = listen()
    if ia_name in text:
        isListening = True
        print("(("+ia_name+" está escuchando))")
        while True:
            response_str = gpt3(text)
            talk(response_str)
            text = listen()
            if ("adiós") or ("Adios") or ("Adiós") or ("adios") or ("Hasta pronto") in text:
                response_str=gpt3(text)
                talk(response_str)
                print("(("+ia_name+" se fue a dormir))")
                isListening = False
                break
    continue