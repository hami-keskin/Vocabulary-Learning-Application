import pyttsx3

speech_engine = pyttsx3.init()

def speak(text):
    speech_engine.say(text)
    speech_engine.runAndWait()

def speak_with_delay(root, text, delay=1000):
    root.after(delay, lambda: speak(text))
