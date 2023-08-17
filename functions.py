#Importing libraries
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import random
import time
import pandas as pd
import webbrowser as wb
import sys
from googlesearch import search
from PyQt6.QtCore import *
import os
# import AppOpener as ao


class Assistant:

    def __init__(self, name): 
        self.name = name #Create instance variable name
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voices',self.voices[1].id)
        self.activationWord = 'Amiy'
    
    def accept_thanks(self):
        ty = ["You are welcome.","Anytime.","It's my duty.","It was a pleasure to help you.","No problem.","Don't mention it"]
        self.speak(ty[random.randint(0,len(ty)-1)])
        
    def greeting(self):
        time = datetime.now().strftime("%H")
        if(int(time) < 12):
            self.speak("Good morning.")
        elif(12<= int(time)<=14):
            self.speak("Good afternoon.")
        elif (14 < int(time) <= 21):
            self.speak("Good evening.")
        else:
            self.speak("Good night.")
        greet = ["Hi!","Hello!", "What's up?","I'm fine."]
        self.speak(greet[random.randint(0,len(greet)-1)])
    
    def meet (self,text):
        txt = text.split()
        self.speak(f"Nice to meet you {txt[len(txt)-1]}, I am Amiy.")

    def leaving(self):
        lv = ["Goodbye!","Take care of yourself.","See you later!","See you soon!","Don't leave me!Haha, it was a joke. Bye bye.","Farewell"]
        self.speak(lv[random.randint(-1,len(lv)-1)])  
        sys.exit()

    def feeling(self):
        fl = ["I'm fine, what about you?","Thanks for asking, you are so kind.","Good, thanks","I don't have feelings actually,but thanks.","Like everytime, I'm fine.",
            "Amazing!","Great!","Normal,you?","I haven't thought about it, next question please."]
        self.speak(fl[random.randint(-1,len(fl)-1)])
    
    def search(self,text):
        url = "https://www.google.com.tr/search?q={}".format(text)
        self.speak("I hope I understood you correctly. Here are the results:")
        wb.open(url)
    
    def browser(self,text): #This function must be improved.
        txt = text[text.index("open")+4:].replace(" ","")   
        
        query = txt
        spk = ["Okay.","I'm on it.",f"Here is {query}."]
        self.speak(spk[random.randint(-1,len(spk)-1)])
        for j in search(query, tld="co.in", stop=1, pause= 0):
            wb.open(j)
        
    def app(self,text):
        from AppOpener import open as o
        txt = text.split()
        self.speak("Shutthefuckup")
        try:
            o(txt[len(txt)-1])
        except Exception as exception:
            self.browser(text)

    def fun(self,text):
        if("sing" in text):
            self.speak("I can do too many things, but I can't sing. Sorry, maybe later.")
        elif("woman" in text or "man" in text):
            self.speak("I mean, isn't it too obvious?? Hm?")
        elif ("who" in text):
            self.speak("I don't know you. If you've said your name, sorry, I forgot it. Because, why not?")
        else:
            from joke_generator import generate
            joke = generate()
            print(joke)
            self.speak(joke)
    
    def time(self):
        time = datetime.now().strftime("%H:%M")
        self.speak(f"Time is {time}")
    
    def suggest(self,text): 
        
        if("movie" in text):
            df =pd.read_csv("imdbTop250.csv")
            lst = df['Title'].to_numpy()
            movie = lst[random.randint(0,6500)]
            url = "https://www.google.com.tr/search?q={}".format(movie)
            self.speak("What I recommend this time is,{} ".format(movie))  
            wb.open(url)     
        elif("music" in text or "song" in text):
            df = pd.read_csv("songs_normalize.csv")
            lst = df['song'].to_numpy()
            music = lst[random.randint(0,2000)]
            url = "https://open.spotify.com/search/{}".format(music)
            self.speak("What I recommend this time is,{} ".format(music))  
            wb.open(url) 

    def reply(self, text):
        from intent_classifier import IntentClassifier
        intent_classifier = IntentClassifier()
        intent = intent_classifier.predict(text)
        replies = {
            "; grace": self.accept_thanks,
            "; search": self.search,
            "; leaving": self.leaving,
            "; feeling": self.feeling,
            "; meet": self.meet,
            "; greeting": self.greeting,
            "; browser":self.browser,
            "; fun": self.fun,
            "; time": self.time,
            "; app": self.app,
            "; suggestion": self.suggest,  
            }

        #Call the dependent function
        from inspect import signature
        reply_func = replies[intent]
        sig = str(signature(reply_func))
        
        if (callable(reply_func) and sig == "()"):
            reply_func()
        elif(callable(reply_func) and sig != "()"):
            reply_func(text)
            
        return intent
            
    
    def speak(self,text, rate = 150):
        self.engine.setProperty('rate',rate)
        self.engine.say(text)
        self.engine.runAndWait()
    
    def getCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
        # r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        
        try:
            text = r.recognize_google(audio)
        except Exception as exception:
            import sys
            self.speak("I couldn't understand you or the command is not proper.")   
            while True:
                said = self.getCommand()
                self.reply(said)

        return text