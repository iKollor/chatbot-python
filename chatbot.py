import openai
import pyttsx3
import speech_recognition as sr
import keys
from gtts import gTTS
import os
#from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
import re

from google.cloud import texttospeech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gKey.json"
client = texttospeech.TextToSpeechClient()

def openfile(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()

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

# start
engine = pyttsx3.init()
listener = sr.Recognizer()
user_input = ""
goodbyes = ["adiós", "adios", "chao", "bye"]

isListening = False

# speech recognition properties (for listen()) #####Theses are the settings for MY microphone Shure sv200 ######
listener.energy_threshold = 100 # default: 3000
listener.dynamic_energy_threshold = True # default: True

#pyttsx3 voice properties
#voices = engine.getProperty("voices")
#engine.setProperty('voice', voices[2].id)
# for voice in voices:
#    print (voice, voice.id)


def gpt3(prompt):
    # using GPT3
    prompt = prompt.encode(encoding="UTF-8", errors="ignore").decode()
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=1, 
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[user_name+":", ia_name+":"]
    )
    response_str = response["choices"][0]["text"].strip()
    return response_str


#def talk(text): # using pyttsx3
    engine.say(text)
    engine.runAndWait()


#def talk(text): # using gTTS
    try:
        tts = gTTS(text=text, lang="es", tld="com.mx" )
        tts.save("voice.mp3")

        audio = AudioSegment.from_mp3("voice.mp3")
        new_file = speedup(audio,1.2,200,10)
        new_file.export("voice_faster.mp3", format="mp3")

        playsound("voice_faster.mp3")
        os.remove("voice.mp3")
        os.remove("voice_faster.mp3")
    except AssertionError:
        print(ia_name+": ¿Puedes repetirme por favor?")
        talk("¿Puedes repetirme por favor?")


#initialize context
context = openfile("prompt_chat.txt")  # open prompt file

def talk(text): # using google cloud tts
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="es-ES", name="es-ES-Wavenet-D", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16, effects_profile_id=["headphone-class-device"]
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open("voice.wav", "wb") as out:
        out.write(response.audio_content)
    
    audio = AudioSegment.from_wav("voice.wav")

    print(ia_name+": "+text)
    play(audio)
    os.remove("voice.wav")


talk("Hola "+user_name+", gracias por terminar la configuración!. Para hablar conmigo di mi nombre. ")


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

    rec_capitalize = rec.capitalize()
    
    return rec_capitalize


print("((Di algo))")
conversation = list()


while True:
    user_input = listen().capitalize() #user input
    if ia_name.lower() in user_input.lower():
        isListening = True
        while True:
            print(user_name+": "+user_input)
            conversation.append(user_name+": %s" % user_input) #add user input to conversation
            text_block = "\n".join(conversation) #make list into text block for GPT3
            words_to_replace = {"<<USER_NAME>>": user_name, "<<IA_NAME>>": ia_name, "<<IA_LANGUAGE>>": ia_language, "<<BLOCK>>":text_block}
            prompt = openfile("prompt_chat.txt")
            for key, value in words_to_replace.items():
                prompt = prompt.replace(key, value)
            prompt = prompt + "\n"+ia_name+": "

            lower_text = user_input.lower()
            split_text = lower_text.split()

            if any(goodbye in split_text for goodbye in goodbyes):
                isListening = False
                break
            
            response_str = gpt3(prompt)#get response from GPT3

            if response_str == "":
                print(ia_name+": ¿Puedes repetirme por favor?")
                talk("¿Puedes repetirme por favor?")
            
            talk(response_str)
            conversation.append(ia_name+": %s" % response_str)
            user_input = listen().capitalize()

        response_str = gpt3(prompt)
        talk(response_str)
        print("(("+ia_name+" se fue a dormir))")
        isListening = False
    else:
        continue
