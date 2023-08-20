import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import tkinter as tk
from threading import Thread
import pyjokes
import pywhatkit
import requests


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty("rate", 130)

root = tk.Tk()
root.title("Voice Assistant")
root.geometry("400x300")
label = tk.Label(root, text="Not Listening", font=("Helvetica", 16))
label.pack(pady=50)

listening = False

def change_label_text(text, color):
    label.config(text=text, fg=color)
    
def listen_for_command():
    global listening
    r = sr.Recognizer()
    with sr.Microphone() as source:
        change_label_text("Listening...", "red")
        speak("Listening")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source, timeout=10)
        change_label_text("Not Listening", "black")

    try:
        change_label_text("Recognizing...", "red")
        speak("Recognizing")
        query = r.recognize_google(audio, language='en-in')
        change_label_text(f"User said: {query}", "black")
        query = query.lower()
        process_query(query)

    except sr.UnknownValueError:
        change_label_text("Sorry, I couldn't understand.", "black")
        speak("Sorry, I couldn't understand.")
        change_label_text("Not Listening", "black")

    listening = False

def get_weather(city_name):
    
    API_KEY='1a184a0294bb959e3d72f0e13ecafabe'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == "404":
        return "City not found."

    weather_data = data.get("weather", [])
    if weather_data:
        weather_description = weather_data[0].get("description", "N/A")
    else:
        weather_description = "N/A"

    temperature = data.get("main", {}).get("temp", "N/A")

    return f"The weather in {city_name} is {weather_description} with a temperature of {temperature}°C."


def process_query(query):
    global listening
    
    if 'wikipedia' in query:
        query = query.replace('wikipedia', '')
        speak("Searching on Wikipedia")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        except Exception as e:
            speak("There was a disambiguation error. Please provide more specific information.")
    elif 'google' in query:
        query = query.replace('google', '')
        speak("Searching on Google")
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)

    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com")
    elif 'open google' in query:
        webbrowser.open("https://www.google.com")
    elif 'open stackoverflow' in query:
        webbrowser.open("https://www.stackoverflow.com")
    
    elif "who made you" in query or "who created you" in query or "who discovered you" in query:
        speak("I was built by Sayan")
    elif 'news' in query:
        news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
        speak('Here are some headlines from the Times of India,Happy reading')
    
    elif 'stop' in query:
        speak('Thanks for your time')
        quit()
    elif 'open flipkart' in query:
        webbrowser.open('flipkart.com')
    
    elif 'weather' in query:
        city_name = query.replace('weather in', '').strip()
        if city_name:
            weather_info = get_weather(city_name)
            speak(weather_info)
        else:
            speak("Please specify a city for weather information.")

    elif 'hello' in query or 'hey' in query or 'whatsup' in query or 'hii' in query:
        speak("Hello! How can I help you?")
    elif 'how are you' in query:
        speak("I'm just a machine, but I'm here and ready to assist!")
    elif 'howdy' in query:
        speak("Howdy! What can I do for you?")
    elif 'nice to meet you' in query:
        speak("Nice to meet you too!")
    elif 'ciao' in query:
        speak("Ciao! How can I assist you today?")
    elif 'good morning' in query:
        speak("Good morning! How can I assist you today?")
    elif 'good afternoon' in query:
        speak("Good afternoon! How can I assist you today?")
    elif 'good evening' in query:
        speak("Good evening! How can I assist you today?")
    elif 'bye' in query:
        speak("Good Bye! Have a nice day")
    else:
        speak("Searching on Google")
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
    
        
    change_label_text("Not Listening", "black")




def start_listening_thread():
    global listening
    if not listening:
        listening = True
        Thread(target=listen_for_command).start()


listen_button = tk.Button(root, text="Start Listening", command=start_listening_thread)
listen_button.pack()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!!")
    else:
        speak("Good Evening!!")
    speak("I am AI developed by Sayan.... i can do the following tasks..... search wikipedia,open stackoverflow,open flipkart, YouTube, Basic Greetings,open google,time,stop to exit the app....How may i help you??")

if __name__ == "__main__":
    wishme()
    root.mainloop()



    