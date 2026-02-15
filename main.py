import flet as ft
import speech_recognition as sr
import pyttsx3
import threading
import requests
import os
from plyer import notification

# --- VEGA CONFIG ---
AI_NAME = "VEGA"
GROQ_API_KEY = "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"

# --- APP DATABASE (Smart Launcher) ---
# Vega in apps ko directly control kar sakta hai
APP_MAP = {
    "whatsapp": "whatsapp://",
    "youtube": "vnd.youtube://",
    "instagram": "instagram://",
    "facebook": "fb://",
    "twitter": "twitter://",
    "chrome": "googlechrome://",
    "gmail": "googlegmail://",
    "maps": "geo:0,0?q=",
    "camera": "camera://",
    "dialer": "tel:",
    "settings": "settings://"
}

class VegaBrain:
    def __init__(self, page):
        self.page = page
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.is_listening = True

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def launch_app(self, app_name):
        # Universal App Launcher Logic
        for key, schema in APP_MAP.items():
            if key in app_name:
                try:
                    self.page.launch_url(schema)
                    return f"Opening {key} protocol."
                except:
                    return f"Error accessing {key}."
        return "App not authorized in database."

    def make_call(self, number):
        # Direct Dialing
        self.page.launch_url(f"tel:{number}")
        return f"Dialing {number}..."

    def listen_loop(self, chat_callback):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    # VEGA Always Listening
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    if "vega" in text:
                        cmd = text.replace("vega", "").strip()
                        chat_callback(f"YOU: {cmd}", True)
                        
                        # 1. APP CONTROL
                        if "open" in cmd:
                            status = self.launch_app(cmd)
                            chat_callback(f"VEGA: {status}", False)
                            self.speak(status)
                        
                        # 2. CALL CONTROL
                        elif "call" in cmd:
                            # Extract number (logic simplified)
                            num = ''.join(filter(str.isdigit, cmd))
                            if num:
                                status = self.make_call(num)
                                chat_callback(f"VEGA: {status}", False)
                                self.speak(status)
                            else:
                                self.speak("Whom should I call, Sir?")

                        # 3. AI BRAIN
                        else:
                            res = self.ask_ai(cmd)
                            chat_callback(f"VEGA: {res}", False)
                            self.speak(res)
                except: pass

    def ask_ai(self, prompt):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        # Updated Personality: VEGA
        sys_msg = "You are VEGA. An aggressive, highly intelligent AI. You control Apps, Calls, and Files. Be precise."
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}]
        }
        try:
            return requests.post(url, headers=headers, json=data).json()['choices'][0]['message']['content']
        except: return "Network Down."

def main(page: ft.Page):
    page.title = "VEGA OS"
    page.bgcolor = "black"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    vega = VegaBrain(page)
    
    # --- VEGA UI (Next Gen) ---
    chat_list = ft.ListView(expand=True, spacing=15, padding=20, auto_scroll=True)
    
    # 1. Holographic Background
    bg_image = ft.Image(
        src="https://i.pinimg.com/originals/e8/1a/c3/e81ac337920dc55f9a72485e78322676.gif",
        fit=ft.ImageFit.COVER,
        opacity=0.3
    )
    
    # 2. Central Core (Animated)
    core = ft.Container(
        content=ft.Icon(ft.icons.FINGERPRINT, size=80, color="purple"),
        width=150, height=150,
        shape=ft.BoxShape.CIRCLE,
        border=ft.border.all(2, "purple"),
        shadow=ft.BoxShadow(blur_radius=50, color="purple"),
        alignment=ft.alignment.center,
        animate_scale=ft.animation.Animation(800, "bounceOut")
    )

    def add_msg(text, is_user):
        color = "white" if is_user else "#D100FF" # Neon Purple for Vega
        align = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        
        chat_list.controls.append(
            ft.Row([
                ft.Container(
                    content=ft.Text(text, color=color, weight="bold", font_family="Consolas"),
                    padding=12,
                    border=ft.border.all(1, color),
                    border_radius=10,
                    bgcolor=ft.colors.with_opacity(0.1, "black")
                )
            ], alignment=align)
        )
        # Animate Core on response
        if not is_user:
            core.scale = 1.2
            core.shadow.color = "cyan"
            page.update()
            time.sleep(0.5)
            core.scale = 1.0
            core.shadow.color = "purple"
        page.update()

    # Start VEGA
    threading.Thread(target=vega.listen_loop, args=(add_msg,), daemon=True).start()

    # UI Stack
    page.add(
        ft.Stack([
            bg_image, # Background
            ft.Column([
                ft.Container(height=40),
                ft.Text("V E G A   S Y S T E M S", size=20, weight="bold", color="purple", letter_spacing=3),
                ft.Text("ACCESS: UNRESTRICTED", size=10, color="green"),
                ft.Container(height=20),
                core, # The Brain
                ft.Container(
                    content=chat_list,
                    expand=True,
                    margin=20,
                    border_radius=20,
                    border=ft.border.only(top=ft.border.BorderSide(1, "purple"))
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ])
    )

ft.app(target=main)
