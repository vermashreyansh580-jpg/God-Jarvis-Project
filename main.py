import flet as ft
import speech_recognition as sr
import threading
import time
from plyer import tts  # 🔥 Native Android Voice Library

# --- VEGA CONFIG ---
WAKE_WORD = "vega"

class GhostVega:
    def __init__(self, page):
        self.page = page
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        try:
            print(f"VEGA: {text}")
            # 🔥 Ye Android ki asli awaaz use karega
            tts.speak(text) 
        except Exception as e:
            print(f"Voice Error: {e}")
            # Agar awaz fail ho, toh screen par likh do
            self.page.snack_bar = ft.SnackBar(ft.Text(f"VEGA: {text}"))
            self.page.snack_bar.open = True
            self.page.update()

    def background_listen(self, visual_feedback):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    # Visual Feedback: Listening (Grey)
                    visual_feedback("LISTENING...", "#222222")
                    
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                    
                    # Visual Feedback: Thinking (Black)
                    visual_feedback("PROCESSING...", "black")
                    
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    if WAKE_WORD in text:
                        # User ka command process karo
                        self.speak("Yes Boss, systems are ready.")
                        
                except:
                    # Agar kuch sunayi na de toh wapas shant ho jao
                    visual_feedback("", "black")
                    pass

def main(page: ft.Page):
    # --- GHOST UI ---
    page.title = "VEGA CORE"
    page.bgcolor = "black"
    page.padding = 0
    # Full Screen Hidden Mode
    page.window_width = 400 
    page.window_height = 800

    vega = GhostVega(page)
    
    # Hidden Text Label
    status_label = ft.Text("TAP TO ACTIVATE", color="#333333", size=15)
    
    # Poori Screen ek Button hai
    bg_container = ft.Container(
        content=status_label,
        expand=True,
        bgcolor="black",
        alignment=ft.alignment.center
    )

    def update_visuals(text, color):
        status_label.value = text
        bg_container.bgcolor = color
        page.update()

    def initialize_system(e):
        status_label.value = "CORE ONLINE"
        status_label.color = "green"
        page.update()
        
        # Pehli Awaaz
        vega.speak("Protocol Initialized. I am listening.")
        
        # Wapas Invisible
        time.sleep(2)
        status_label.value = ""
        status_label.color = "black"
        page.update()
        
        # Background Listening Start
        threading.Thread(target=vega.background_listen, args=(update_visuals,), daemon=True).start()

    bg_container.on_click = initialize_system
    page.add(bg_container)

ft.app(target=main)
