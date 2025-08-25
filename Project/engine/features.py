from playsound import playsound
import eel
# Playing assistant sound function
@eel.expose
def playAssistantSound():
    music_dir = r"C:\Users\Noah\Desktop\python\sem prep\Project\Frontend\assets\audio\start_sound.mp3"
    playsound(music_dir)
    