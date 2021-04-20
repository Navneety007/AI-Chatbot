import datetime
from chatterbot.utils import get_response_time
import speech_recognition as sr
import pyttsx3
import random
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import os
import webbrowser
from youtube_search import YoutubeSearch
from googlesearch import search
import wikipedia
import pyautogui
import pyjokes
import time


with open("trainbot.txt","r") as train:
    data = train.read().splitlines()

chatbot = ChatBot("Alicia")
trainer = ChatterBotCorpusTrainer(chatbot)
listtrainer = ListTrainer(chatbot)
listtrainer.train(data)
trainer.train("chatterbot.corpus.english.greetings", 
              "chatterbot.corpus.english.conversations" )

engine = pyttsx3.init()
voice = engine.getProperty('voices')
engine.setProperty('voice',voice[1].id)
engine.setProperty('rate',200)


def speak(query):
    engine.say(query)
    engine.runAndWait()

def wishing():
    hour = datetime.datetime.now().hour
    if hour>= 6 and hour <= 12:
        speak("Good Morning Sire , How can i help you at the moment")
    elif hour>= 12 and hour <= 16:
        speak("Good Afternoon Sire , How can i help you at the moment")
    elif hour>= 16 and hour <= 22:
        speak("Good Evening Sire , How can i help you at the moment")
    else:
        speak("Good Night Sire , I would prefer ya to sleep at the moment")



def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration = 1)
        print("Speak sir!")
        audio = r.listen(source)
    try:
        print(r.recognize_google(audio,language = "en-US"))
        query = r.recognize_google(audio,language = "en-US")
    except:
        print("Sorry couldn't recognize , could you speak that again?")
        speak("Sorry couldn't recognize , could you speak that again?")
        command()

    return query
wishing()
while True:
    query = command()
    query = query.lower()
    if "your name" in query:
        speak("My name is alicia")
        print("My name is alicia")
        pass
    
    elif "joke" in query:
        joke = random.choice(pyjokes.get_jokes())
        print(joke)
        speak(joke)

    elif "screenshot" in query:
        img = pyautogui.screenshot()
        img.save("ss.png")
        speak("Screenshot Taken")
        pass

    elif "stop listening" in query:
        speak("For how many minutes do you want me to sleep")
        print("For how many minutes do you want me to sleep")

        try:
            query = command()
            query = float(query)
        except:
            speak("Please specify the amount alone")
            print("Example - 1 , 2000 , 0.1 (minutes)")
            
            query = command()
            query = float(query)

        speak("ok")
        time.sleep(query*60)
        speak("I'm Back")
        pass

    

    elif "search google" in query:
        speak("WHat do you wanna search sire?")
        print("WHat do you wanna search sire?")

        query = command()
        query = query.lower()

        result = search(query,num_results=3)
        webbrowser.open(result[0])
        print(*result,sep="\n")
        speak("opening Google")

    elif "search youtube" in query:
        speak("WHat do you wanna watch sire?")
        print("WHat do you wanna watch sire?")

        query = command()
        query = query.lower()

        result = YoutubeSearch(query,max_results=1).to_dict()
        result = result[0]["url_suffix"]
        result = "youtube.com"+result
        webbrowser.open(result)
        speak("opening Youtube")

    elif "wikipedia" in query:
        speak("WHat do you wanna wikipedia?")
        print("WHat do you wanna wikipedia?")

        query = command()
        query = query.lower()

        result = wikipedia.summary(query,sentences = 3)
        print(result)
        speak("According to Wikipedia , " + result)

    elif "listen music" in query:
        speak("WHat do you wanna listen?")
        print("WHat do you wanna listen?")

        query = command()
        query = query.lower()

        songlink = "https://open.spotify.com/search/"+query
        webbrowser.open(songlink)
        speak("Opening Spotify")


    elif "open notepad" in query:
        speak("Openeing Notepad")
        os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\notepad")
        pass
    elif "shutdown" in query:
        if input("Are u sure wanna shutdown(press enter to proceed) : ") == "":
            speak("shutting down the system")
            os.system("shutdown /s /t 1")
        pass
    elif "log out" in query:
        if input("Are u sure wanna Log off(press enter to proceed) : ") == "":
            speak("Logging off the system")
            os.system("shutdown -1")
        pass
    elif "restart" in query:
        if input("Are u sure wanna restart(press enter to proceed) : ") == "":
            speak("Restarting the system")
            os.system("shutdown /r /t 1")
        pass
    elif "go offline" in query:
        speak("Going offline now")
        print("Sayonara")
        quit()
    else: 
        response = str(chatbot.get_response(query))
        with open("trainbot.txt","a") as train:
            train.write(query+"\n"+response+"\n")

        listtrainer.train([query,response])
        print(response)
        speak(response)

