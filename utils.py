import tkinter as tk

import pyttsx3
import pyperclip
from datetime import datetime

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


def mark_memorized(current_data, next_word):
    current_data["memorized"] = True
    next_word()

def mark_known(current_data, next_word):
    current_data["known"] = True
    current_data["correct_streak"] = 0
    next_word()

def add_to_retry(current_data, next_word):
    current_data.update({"retry": True, "correct_streak": 0, "date": get_today()})
    next_word()

def show_notification(root, message, duration=2000):
    """Geçici bir bilgi etiketi gösterir."""
    notification_label = tk.Label(root, bg="yellow", fg="black", font=("Arial", 12), pady=5)
    notification_label.pack_forget()  # Başlangıçta gizlenir
    notification_label.config(text=message)
    notification_label.pack(side=tk.TOP, fill=tk.X)
    root.after(duration, lambda: notification_label.pack_forget())
