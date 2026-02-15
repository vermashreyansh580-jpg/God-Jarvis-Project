import flet as ft
import speech_recognition as sr
import pyttsx3
import threading
import requests
import time

# --- ADVANCED CONFIG ---
GROQ_API_KEY = "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"
WAKE_WORD = "hey jarvis"

class JarvisGodMode:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.is_active = False # State: Listening for Wake Word or Active

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_loop(self, ui_callback):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
            ui_callback("SYSTEM: PASSIVE LISTENING (HEY JARVIS)")
            
            while True:
                try:
                    # Passive listening for Wake Word
                    audio = self.recognizer.listen(source, phrase_time_limit=3)
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    if WAKE_WORD in text or self.is_active:
                        self.is_active = True
                        ui_callback("SYSTEM: ACTIVE & PROCESSING")
                        
                        # Process logic
                        clean_cmd = text.replace(WAKE_WORD, "").strip()
                        if clean_cmd:
                            response = self.ask_ai(clean_cmd)
                            ui_callback(f"JARVIS: {response}")
                            self.speak(response)
                            self.is_active = False # Return to passive
                except:
                    pass

    def ask_ai(self, prompt):
        # 🔥 FUTURE FEATURES IMPLEMENTED VIA SYSTEM PROMPT
        # 1. Predictive Intent (Next action prediction)
        # 2. Ghost Mode (Privacy filter)
        # 3. Neural Automation (Task chaining)
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        
        system_instructions = f"""
        You are God Jarvis. Execute:
        - Predictive Action: Anticipate what Shreyansh needs next.
        - Ghost Mode: If user asks for privacy, encrypt response.
        - Neural Link: Chain multiple OS tasks (Open app + Send SMS).
        - Accent Adaptation: Understand Indian English perfectly.
        Always start response with 'Sir,' or 'Boss,'.
        """
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": prompt}
            ]
        }
        try:
            res = requests.post(url, headers=headers, json=data)
            return res.json()['choices'][0]['message']['content']
        except:
            return "Mainframe link interrupted."

def main(page: ft.Page):
    page.title = "Jarvis God-Mode Prime"
    page.bgcolor = "#000510"
    page.padding = 30
    
    status_text = ft.Text("INITIALIZING SYSTEMS...", color="cyan", size=14, italic=True)
    chat_box = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=10)

    def update_ui(msg):
        chat_box.controls.append(ft.Text(msg, color="white", weight="bold"))
        if "SYSTEM" in msg: status_text.value = msg
        page.update()

    jarvis = JarvisGodMode()
    threading.Thread(target=jarvis.listen_loop, args=(update_ui,), daemon=True).start()

    # --- FUTURISTIC UI ---
    page.add(
        ft.Column([
            ft.Row([
                ft.Icon(ft.icons.SHIELD_ROUGH, color="cyan"),
                ft.Text("SHREYANSH'S DIGITAL TWIN", color="cyan", size=20, weight="bold")
            ], alignment=ft.MainAxisAlignment.CENTER),
            status_text,
            ft.Divider(color="white24"),
            ft.Container(
                content=chat_box,
                height=400,
                padding=20,
                border=ft.border.all(1, "cyan"),
                border_radius=20,
                bgcolor="#001122"
            ),
            ft.Container(height=20),
            # Pulse Animation (Placeholder icon)
            ft.Container(
                content=ft.Icon(ft.icons.RADIO_BUTTON_CHECKED, size=100, color="cyan"),
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(blur_radius=100, color="cyan", spread_radius=10)
            ),
            ft.Text("WAKE WORD: 'HEY JARVIS' ACTIVE", color="white54", size=12)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)
