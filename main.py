import flet as ft
import speech_recognition as sr
import pyttsx3
import threading
import time

# --- VEGA CONFIG ---
WAKE_WORD = "vega"

class GhostVega:
    def __init__(self, page):
        self.page = page
        # Safe Initialization
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 170)
        except:
            print("TTS Engine Failed to Init")
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        try:
            print(f"VEGA: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Voice Error: {e}")
            # Agar awaz fail ho, toh screen par likh do (Fallback)
            self.page.snack_bar = ft.SnackBar(ft.Text(f"VEGA: {text}"))
            self.page.snack_bar.open = True
            self.page.update()

    def background_listen(self, visual_feedback):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    # Visual Feedback: Listening Mode (Dark Grey)
                    visual_feedback("LISTENING...", "#111111")
                    
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                    
                    # Visual Feedback: Processing (Pitch Black)
                    visual_feedback("PROCESSING...", "black")
                    
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    if WAKE_WORD in text:
                        self.speak("At your service, Boss.")
                        # Yahan Action Logic aayega
                        
                except Exception as e:
                    # Agar kuch na sunayi de, wapas black kar do
                    visual_feedback("", "black")
                    pass

def main(page: ft.Page):
    # --- GHOST UI ---
    page.title = "VEGA CORE"
    page.bgcolor = "black"
    page.padding = 0
    
    # Isse app full screen lega par dikhega nahi
    page.window_width = 400 
    page.window_height = 800

    vega = GhostVega(page)
    
    status_label = ft.Text("TAP TO ACTIVATE VEGA", color="#222222", size=15)
    
    # Screen ka background change karne ke liye container ref
    bg_container = ft.Container(
        content=status_label,
        expand=True,
        bgcolor="black",
        alignment=ft.alignment.center
    )

    def update_visuals(text, color):
        # Thread se UI update karne ke liye safe tarika
        status_label.value = text
        bg_container.bgcolor = color
        page.update()

    def initialize_system(e):
        status_label.value = "CORE ONLINE"
        status_label.color = "#00FF00" # Green text for 1 second
        page.update()
        
        # Bolne ke baad wapas invisible ho jayega
        vega.speak("System Online.")
        status_label.color = "#111111" # Almost invisible
        page.update()
        
        # Thread Start
        threading.Thread(target=vega.background_listen, args=(update_visuals,), daemon=True).start()

    # Click event container par lagaya hai
    bg_container.on_click = initialize_system

    page.add(bg_container)

ft.app(target=main)
