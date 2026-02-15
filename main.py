import flet as ft
import speech_recognition as sr
import pyttsx3
import threading
import time

# --- VEGA CONFIG ---
WAKE_WORD = "vega"

class GhostVega:
    def __init__(self):
        self.engine = pyttsx3.init()
        # Voice Settings (Robotic/Fast)
        self.engine.setProperty('rate', 170)
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except:
            pass

    def background_listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    # Hamesha sunta rahega (Green Dot On rahega)
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    if WAKE_WORD in text:
                        self.speak("Yes Boss?")
                        # Yahan tumhara AI logic aayega (API call etc.)
                        print(f"User said: {text}")
                except:
                    pass

def main(page: ft.Page):
    # --- STEALTH UI ---
    page.title = "VEGA SERVICE"
    page.bgcolor = "black"  # Poora screen kaala
    page.padding = 0
    page.window_width = 0   # Koshish karega invisible hone ki
    page.window_height = 0

    vega = GhostVega()

    def start_system(e=None):
        # 1. Pehle bolega
        vega.speak("System is Online, Boss.")
        
        # 2. Fir background thread shuru
        threading.Thread(target=vega.background_listen, daemon=True).start()
        
        # 3. Screen par "Core Active" likha aayega (Black on Black - Invisible)
        page.add(ft.Text("CORE ACTIVE", color="black"))
        page.update()

    # Permissions Trigger Button (Sirf pehli baar dikhega agar theme alag ho)
    # Background black hai, button bhi black/dark grey hoga.
    start_btn = ft.ElevatedButton(
        "INITIALIZE", 
        on_click=start_system,
        bgcolor="#111111", # Almost black
        color="#333333"    # Very dark grey
    )

    page.add(
        ft.Container(
            content=start_btn,
            alignment=ft.alignment.center,
            margin=ft.margin.only(top=300)
        )
    )

    # Auto-Click logic (App khulte hi start karne ki koshish)
    # Note: Android permissions maangne ke liye user interaction zaroori hota hai
    # Isliye pehli baar button dabana padega, uske baad ye automatic lagega.
    
ft.app(target=main)
