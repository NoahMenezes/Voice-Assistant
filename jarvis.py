import sys
import os
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import subprocess
import wikipedia
import psutil  # For battery & CPU info
import pyautogui  # For volume/brightness keys
import pywhatkit as kit  # For YouTube & Google fallback

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QMetaObject, Qt
from threading import Thread

# ------------------ Voice Setup ------------------
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)   # 0 = male
engine.setProperty("rate", 170)

apps = {
    "notepad": "notepad",
    "calculator": "calc",
}

memory = {"last_command": None}

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙 Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"You said: {query}")
    except:
        return "None"
    return query.lower()

def open_app(app_name):
    if app_name in apps:
        os.system(f"start {apps[app_name]}")
        memory["last_command"] = f"Opened {app_name}"
    else:
        speak("App not found")

def execute_task(query):
    memory["last_command"] = query

    if "time" in query:
        speak(f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}")

    elif "date" in query:
        speak(f"Today is {datetime.datetime.now().strftime('%A, %d %B %Y')}")

    elif "open youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open google" in query:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "search youtube" in query:
        topic = query.replace("search youtube", "").strip()
        speak(f"Searching YouTube for {topic}")
        kit.playonyt(topic)

    elif "wikipedia" in query:
        topic = query.replace("wikipedia", "").strip()
        try:
            result = wikipedia.summary(topic, sentences=2)
            speak(result)
        except:
            speak(f"No result on Wikipedia, searching Google for {topic}")
            kit.search(topic)

    elif "battery" in query:
        battery = psutil.sensors_battery()
        if battery:
            speak(f"Battery is at {battery.percent} percent")
        else:
            speak("Battery information not available")

    elif "volume up" in query:
        pyautogui.press("volumeup")
        speak("Volume increased")

    elif "volume down" in query:
        pyautogui.press("volumedown")
        speak("Volume decreased")

    elif "mute" in query:
        pyautogui.press("volumemute")
        speak("Volume muted")

    elif "open" in query:
        app_name = query.replace("open", "").strip()
        open_app(app_name)

    elif "last command" in query:
        if memory["last_command"]:
            speak(f"Your last command was: {memory['last_command']}")
        else:
            speak("I don't remember your last command")

    elif "shutdown" in query:
        speak("Shutting down your system")
        os.system("shutdown /s /t 5")

    elif "restart" in query:
        speak("Restarting system")
        os.system("shutdown /r /t 5")

    elif "exit" in query or "quit" in query:
        speak("Goodbye Noah")
        sys.exit()

    else:
        speak("Sorry, I didn't understand that. Should I search it?")
        kit.search(query)

def voice_loop():
    speak("Hello Noah, I am Jarvis. Say 'Hey Jarvis' to wake me up.")
    while True:
        query = take_command()
        if "jarvis" in query:   # wake word check
            speak("Yes, I'm listening.")
            query = take_command()
            if query != "None":
                execute_task(query)

# ------------------ GUI ------------------
class JarvisUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis Assistant")
        self.setGeometry(100, 100, 900, 600)

        self.browser = QWebEngineView()
        html_path = os.path.abspath("jarvis_ui.html")  # your design file
        self.browser.setUrl(QUrl.fromLocalFile(html_path))

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = JarvisUI()
    window.show()

    # Run assistant in a background thread
    t = Thread(target=voice_loop, daemon=True)
    t.start()

    sys.exit(app.exec_())
