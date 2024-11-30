import pyttsx3
import pyperclip
from datetime import datetime, timedelta

speech_engine = pyttsx3.init()

def speak(text):
    speech_engine.say(text)
    speech_engine.runAndWait()

def speak_with_delay(text, root, delay=1000):
    root.after(delay, lambda: speak(text))

def copy_to_clipboard(text):
    pyperclip.copy(text)

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d")

def get_today():
    return format_date(datetime.now())
