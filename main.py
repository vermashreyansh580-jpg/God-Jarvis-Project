import flet as ft
import speech_recognition as sr
import pyttsx3
import threading
import requests
import time
import math

# --- CONFIG ---
GROQ_API_KEY = "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"

class JarvisBrain:
    def __init__(self, page):
        self.page = page
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.is_listening = True

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def animate_reactor(self, is_talking):
        # Pulse Animation logic
        scale = 1.2 if is_talking else 1.0
        shadow = 50 if is_talking else 20
        self.page.reactor.scale = scale
        self.page.reactor.shadow.blur_radius = shadow
        self.page.update()

    def listen_loop(self, chat_callback):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            while True:
                try:
                    # Green Dot Active
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio).lower()
                    
                    chat_callback(f"YOU: {text}", is_user=True)
                    
                    if "jarvis" in text:
                        self.animate_reactor(True) # Glow Effect ON
                        response = self.ask_ai(text)
                        chat_callback(f"JARVIS: {response}", is_user=False)
                        self.speak(response)
                        self.animate_reactor(False) # Glow Effect OFF
                except:
                    pass

    def ask_ai(self, prompt):
        # IN-APP CONTROLS
        if "clear" in prompt: return "CLEAR_LOGS"
        if "red theme" in prompt: return "THEME_RED"
        if "blue theme" in prompt: return "THEME_BLUE"

        # AI BRAIN
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": "You are Jarvis. Be cool, futuristic, and concise."},
                         {"role": "user", "content": prompt}]
        }
        try:
            return requests.post(url, headers=headers, json=data).json()['choices'][0]['message']['content']
        except: return "Server uplink failed."

def main(page: ft.Page):
    page.title = "God Jarvis HUD"
    page.bgcolor = "#000510" # Deep Space Black
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    
    # --- UI COMPONENTS ---
    
    # 1. Background Gradient (Cyberpunk Look)
    background = ft.Container(
        expand=True,
        gradient=ft.RadialGradient(
            center=ft.alignment.center,
            radius=1.5,
            colors=["#001F3F", "#000000"],
        )
    )

    # 2. Chat Area (Glassmorphism)
    chat_list = ft.ListView(expand=True, spacing=15, padding=20, auto_scroll=True)
    
    chat_container = ft.Container(
        content=chat_list,
        height=400,
        margin=ft.margin.symmetric(horizontal=20),
        padding=10,
        border_radius=20,
        border=ft.border.all(1, color=ft.colors.with_opacity(0.3, "cyan")),
        bgcolor=ft.colors.with_opacity(0.1, "black"), # Glass effect
        blur=ft.Blur(10, 10)
    )

    # 3. The Arc Reactor (Animated Button)
    reactor_icon = ft.Icon(ft.icons.POWER_SETTINGS_NEW, size=60, color="cyan")
    
    reactor = ft.Container(
        content=reactor_icon,
        width=120, height=120,
        border_radius=60,
        border=ft.border.all(4, "cyan"),
        bgcolor=ft.colors.with_opacity(0.1, "cyan"),
        shadow=ft.BoxShadow(blur_radius=20, color="cyan", spread_radius=2),
        animate_scale=ft.animation.Animation(500, ft.AnimationCurve.BOUNCE_OUT),
        alignment=ft.alignment.center,
        on_click=lambda _: page.snack_bar.show()
    )
    page.reactor = reactor # Store for animation access

    # --- LOGIC HANDLING ---
    brain = JarvisBrain(page)

    def add_message(msg, is_user):
        # Special In-App Commands
        if msg == "JARVIS: CLEAR_LOGS":
            chat_list.controls.clear()
            page.update()
            return
        if msg == "JARVIS: THEME_RED":
            reactor_icon.color = "red"
            reactor.border.border_side.color = "red"
            reactor.shadow.color = "red"
            page.update()
            return

        # Chat Bubble Design
        align = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        color = "white" if is_user else "cyan"
        bg_color = ft.colors.with_opacity(0.2, "white") if is_user else ft.colors.with_opacity(0.2, "cyan")
        
        bubble = ft.Row([
            ft.Container(
                content=ft.Text(msg, color=color, weight="bold", font_family="Courier"),
                padding=15,
                border_radius=15,
                bgcolor=bg_color,
                border=ft.border.all(1, color)
            )
        ], alignment=align)
        
        chat_list.controls.append(bubble)
        page.update()

    # Start Background Voice
    threading.Thread(target=brain.listen_loop, args=(add_message,), daemon=True).start()

    # --- FINAL LAYOUT ---
    ui_layer = ft.Column([
        ft.Container(height=50),
        ft.Text("J.A.R.V.I.S  P.R.I.M.E", size=24, weight="bold", color="cyan", letter_spacing=5, text_align="center"),
        ft.Text("SYSTEM STATUS: ONLINE | MIC: ACTIVE", size=10, color="green"),
        ft.Container(height=20),
        reactor,
        ft.Container(height=30),
        chat_container,
        ft.Container(height=20),
        ft.Text("DESIGNED BY SHREYANSH", color="white24", size=10)
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(ft.Stack([background, ui_layer]))

ft.app(target=main)
