import openai
import pyttsx3
import speech_recognition as sr
import keys

# api-key
openai.api_key = keys.api_key

# setMic
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
mic = sr.Microphone(device_index=1)

# input
user_name_raw = input("Escribe tu nombre: ")
user_name = user_name_raw.capitalize()
ia_name_raw = input("Escribe el nombre de la IA: ")
ia_name = ia_name_raw.capitalize()
ia_language_raw = input("Escribe el idioma de la IA: ")
ia_language = ia_language_raw.lower()

#initialize context
context = ia_name + " es una asistente virtual que solo habla "+ ia_language +". "+ia_name+" es muy sarcástica, bromista y servicial a "+user_name+"."
#input("Describe a tu IA: ")
print(context)

# start
engine = pyttsx3.init()
listener = sr.Recognizer()
text = ""
conversation = ""

isListening = False

# sr properties
listener.energy_threshold = 100
listener.dynamic_energy_threshold = False
# sr voice properties
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[2].id)
# for voice in voices:
#    print (voice, voice.id)


def gpt3(text, conversation):
    # using GPT3
    prompt = user_name + ": " + text + "\n"+ia_name+": "
    print(user_name+": "+text)
    conversation += prompt
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=(context+"\n\n"+conversation),
        temperature=0.9, 
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[user_name+":"]
    )
    response_str = response["choices"][0]["text"].replace(ia_name+":", "").strip()
    conversation += response_str
    print(ia_name+": "+response_str)
    return response_str


def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():

    if isListening == True:
        print("(("+ia_name+" está escuchando))")
    else:
        print("(("+ia_name+" no está escuchando))")

    with mic as source:
        listener.adjust_for_ambient_noise(source, duration=0.3)
        voice = listener.listen(source)
        print("((Hablaste))")

    try:
        rec = listener.recognize_google(voice, language="es-ES")
    except:
        rec = "*"+user_name+" dice algo inentendible*"
    return rec


print("((Di algo))")

while True:
    text = listen()
    if ia_name in text:
        isListening = True
        while ("adiós" or "adios") not in text.lower():

            response_str = gpt3(text, conversation)

            if response_str == " ":
                print(ia_name+": ¿Puedes repetirme por favor?")
                talk("¿Puedes repetirme por favor?")
            
            talk(response_str)
            text = listen()

        response_str = gpt3(text, conversation)
        talk(response_str)
        print("(("+ia_name+" se fue a dormir))")
        isListening = False
    else:
        continue
