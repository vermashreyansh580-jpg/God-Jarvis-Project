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
        self.engine.setProperty('rate', 170) # Fast robotic voice
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        try:
            print(f"VEGA: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except:
            pass

    def background_listen(self):
        # Continuous Listening Loop
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    # Green Dot will remain active here
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    if WAKE_WORD in text:
                        self.speak("Listening Boss...")
                        # Yahan tumhara Action Logic aayega
                except:
                    pass

def main(page: ft.Page):
    # --- GHOST UI (INVISIBLE) ---
    page.title = "VEGA CORE"
    page.bgcolor = "black"  # Pitch Black
    page.padding = 0
    page.window_width = 0
    page.window_height = 0
    
    vega = GhostVega()
    
    # Status Text (Sirf Debugging ke liye, user ko barely dikhega)
    status_label = ft.Text("SYSTEM BOOT...", color="#111111", size=10)

    def initialize_system(e=None):
        # 1. Update Status
        status_label.value = "CORE ACTIVE"
        page.update()
        
        # 2. Voice Feedback
        vega.speak("System is Online, Boss.")
        
        # 3. Start Mic Thread
        threading.Thread(target=vega.background_listen, daemon=True).start()

    # Invisible Button (Full Screen Click)
    # Android requires interaction to start Audio
    start_btn = ft.Container(
        content=status_label,
        width=1000, height=2000, # Covers whole screen
        bgcolor="black",
        on_click=initialize_system,
        alignment=ft.alignment.center
    )

    page.add(start_btn)

ft.app(target=main)
