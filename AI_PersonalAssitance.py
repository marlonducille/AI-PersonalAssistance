#https://towardsdatascience.com/how-to-build-your-own-ai-personal-assistant-using-python-f57247b4494b

import speech_recognition as sr
import pyttsx3 
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests

#----------------------------

# SETTING UP THE SPEECH ENGINE

#-----------------------------

#pyttxs3 is a text to speech conversion library in python. This package supports text to speech engines on Mac os x, Windows and on Linux.

#Sapi5 is a Microsoft Text to speech engine used for voice recognition.
#The voice Id can be set as either 0 or 1,
#0 indicates Male voice
#1 indicates Female voice

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')

#converts text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()
    
#--------------------------------------

# INITITATE FUNCTION TO GREET THE USER

#--------------------------------------

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")
        

#---------------------------------------------

# SETTING UP COMMAND FUNCTION FOR AI ASSISTANT

#---------------------------------------------

# Define a function takecommand for the AI assistant to understand and to accept human language. 
# The microphone captures the human speech and the recognizer recognizes the speech to give a response.

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)

        try:
            #recognize_google function uses google audio to recognize speech.
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement

print("Loading your AI personal assistant G-One")
speak("Loading your AI personal assistant G-One")
wishMe()

#-----------------

# MAIN FUNCTION

#----------------

# __name__ == “main” is used to execute some code only if the file was run directly, and not imported
# __name__ is a built-in variable which evaluates to the name of the current module
# '__main__' is the name of the scope in which top-level code executes. 
# A module's __name__ is set equal to '__main__' when read from standard input, a script, or from an interactive prompt.
if __name__=='__main__':
    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand().lower()
        if statement==0:
            continue
        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('your personal assistant G-one is shutting down,Good bye')
            print('your personal assistant G-one is shutting down,Good bye')
            break
        #Fetching data from Wikipedia:
        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement =statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        #Accessing the Web Browsers — Google chrome , G-Mail and YouTube:
        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(5)
        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")
            time.sleep(5)
        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            time.sleep(5)
        #Predicting time
        elif 'time' in statement:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")
        #To fetch latest news
        elif 'news' in statement:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India,Happy reading')
            time.sleep(6)            
        #Capturing photo
        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0,"robo camera","img.jpg")
        #Searching data from web
        elif 'search'  in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)
        #Setting your AI assistant to answer geographical and computational questions
        elif 'ask' in statement:
            speak('I can answer to computational and geographical questions  and what question do you want to ask now')
            question=takeCommand()
            app_id="Paste your unique ID here "
            client = wolframalpha.Client('AWGLUE-WKXPWA78LK') 
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)
        #To forecast weather:
        elif "weather" in statement:
            api_key="293ffd620dc8b4192a8b86b35ee48b4e"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("what is the city name")
            city_name=takeCommand()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))



