import pyttsx3
import speech_recognition as sr
import eel
import threading
def speak(text):   #speak the text
    engine=pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id) # voice speaker, 0->male,1->female
    engine.setProperty('rate', 125) # voice speed
    print(voices)
    engine.say(text)
    engine.runAndWait()
    
@eel.expose
def takecommand():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:   # ✅ added () after Microphone
            print("Listening....")
            eel.DisplayMessage("Listening....")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)

            # ✅ safer listen: no timeout crash
            audio = r.listen(source, timeout=5, phrase_time_limit=6)

        print("Recognizing....")
        eel.DisplayMessage("Recognizing....")
        query = r.recognize_google(audio, language="en-IN")  # en-IN is correct
        print(f'User said: {query}')
        eel.DisplayMessage(query)

        # run speak in separate thread so eel doesn’t freeze
        threading.Thread(target=speak, args=(query,), daemon=True).start()

        return query.lower()

    except sr.WaitTimeoutError:
        print("⏳ Timeout: No speech detected")
        eel.DisplayMessage("Timeout: No speech detected")
        return ""

    except sr.UnknownValueError:
        print("❌ Could not understand audio")
        eel.DisplayMessage("Could not understand audio")
        return ""

    except sr.RequestError as e:
        print("⚠️ Could not request results; check internet:", repr(e))
        eel.DisplayMessage("Internet error")
        return ""

    except Exception as e:
        print("Recognition failed:", repr(e))
        eel.DisplayMessage("Recognition failed")
        return ""
        
