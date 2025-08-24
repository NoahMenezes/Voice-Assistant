import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import wikipedia
import subprocess

# ------------------ Setup ------------------
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)   # 0 = male, 1 = female
engine.setProperty("rate", 170)             # speaking speed

# Browser paths (update if your Chrome/Edge is installed elsewhere)
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
edge_path   = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s"

# Predefined apps (you can add more here)
apps = {
    "notepad": "notepad",
    "calculator": "calc",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vs code": r"C:\Users\Noah\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "spotify": r"C:\Users\Noah\AppData\Roaming\Spotify\Spotify.exe",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
}

# Path for the futuristic HTML UI (make sure this file exists!)
html_ui_path = os.path.abspath("jarvis_ui.html")  # save your HTML as jarvis_ui.html in same folder

def speak(text):
    """Make Jarvis speak"""
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Take voice input and convert to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙 Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)  # handle noise
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"You said: {query}")
    except sr.UnknownValueError:
        print("❌ Could not understand, please repeat...")
        return "None"
    except sr.RequestError:
        print("⚠️ Network error.")
        return "None"

    return query.lower()

def wish_me():
    """Wish user based on time"""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning Noah!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Noah!")
    else:
        speak("Good Evening Noah!")
    speak("I am Jarvis. How can I assist you today?")

def open_browser(url):
    """Try opening with Chrome, else Edge, else fallback"""
    try:
        webbrowser.get(chrome_path).open(url)
        print(f"✅ Opened with Chrome: {url}")
    except:
        try:
            webbrowser.get(edge_path).open(url)
            print(f"✅ Opened with Edge: {url}")
        except:
            webbrowser.open(url)
            print(f"✅ Opened with default browser: {url}")

def open_app(app_name):
    """Open apps from predefined list or using system command"""
    if app_name in apps:
        speak(f"Opening {app_name}...")
        try:
            os.startfile(apps[app_name])
        except Exception:
            subprocess.Popen(apps[app_name], shell=True)
    else:
        try:
            speak(f"Trying to open {app_name}...")
            os.system(f"start {app_name}")
        except Exception:
            speak(f"Sorry, I couldn't find {app_name} on your system.")

def execute_task(query):
    """Perform tasks based on voice command"""
    print(f"DEBUG: Inside execute_task with query = {repr(query)}")

    if "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")

    elif "date" in query:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today's date is {today}")

    elif "open youtube" in query:
        speak("Opening YouTube...")
        open_browser("https://youtube.com")

    elif "open google" in query:
        speak("Opening Google...")
        open_browser("https://google.com")

    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "").strip()
        try:
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(result)
            speak(result)
        except Exception:
            speak("Sorry, I couldn't find anything on Wikipedia.")

    elif "play music" in query:
        music_dir = "C:\\Users\\Noah\\Music"   # change path if needed
        try:
            songs = os.listdir(music_dir)
            if songs:
                speak("Playing music...")
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No music files found in your music folder.")
        except FileNotFoundError:
            speak("Music folder not found, please update the path.")

    elif "open" in query:
        app_name = query.replace("open", "").strip()
        open_app(app_name)

    elif "exit" in query or "quit" in query or "goodbye" in query:
        speak("Goodbye Noah, shutting down.")
        exit()

    else:
        speak("Sorry, I didn't understand that. Could you repeat?")

# ------------------ Main ------------------
if __name__ == "__main__":
    # Open the futuristic UI when Jarvis starts
    if os.path.exists(html_ui_path):
        webbrowser.open(f"file:///{html_ui_path}")
    else:
        print(f"⚠️ HTML UI file not found at {html_ui_path}. Please save your design as 'jarvis_ui.html'.")

    wish_me()
    while True:
        query = take_command()
        if query != "None":
            execute_task(query)
