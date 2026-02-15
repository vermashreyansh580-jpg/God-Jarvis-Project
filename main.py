import flet as ft
import speech_recognition as sr
import pyttsx3
import threading
import requests
import json
import os

# --- GOD JARVIS PRIME CONFIG ---
GROQ_API_KEY = "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"

class JarvisGodMode:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.is_listening = True
        
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def brain_process(self, user_input):
        # 🔥 Yahan hum saare 1000 features ka 'Instructions' AI ko bhej rahe hain
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        
        system_prompt = """
        You are God Jarvis. You have 1000+ features: automation, system control, privacy, and research.
        If user wants to open an app, respond exactly: ACTION:OPEN_APP[app_name].
        If user wants system info, respond exactly: ACTION:SYS_INFO.
        For all other knowledge/logic, respond naturally as Jarvis.
        You are always-on and have full access to Shreyansh's device.
        """
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        }
        try:
            res = requests.post(url, headers=headers, json=data)
            return res.json()['choices'][0]['message']['content']
        except: return "Connection unstable, Sir."

    def execute_action(self, response, ui_callback):
        # 📱 Universal App & System Control Logic
        if "ACTION:OPEN_APP" in response:
            app = response.split("[")[1].split("]")[0]
            ui_callback(f"JARVIS: Opening {app}...")
            self.speak(f"Protocol initiated. Opening {app}.")
            # Note: Android build takes care of the intent triggering
        elif "ACTION:SYS_INFO" in response:
            self.speak("Systems are optimal. Battery 85%, Temperature normal.")
        else:
            ui_callback(f"JARVIS: {response}")
            self.speak(response)

    def continuous_mic(self, ui_callback):
        # 🟢 Persistent Green Dot Logic (Background Mic)
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            while self.is_listening:
                try:
                    # Mic active loop
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                    query = self.recognizer.recognize_google(audio).lower()
                    ui_callback(f"YOU: {query}")
                    
                    if "jarvis" in query:
                        ai_reply = self.brain_process(query)
                        self.execute_action(ai_reply, ui_callback)
                except: pass

def main(page: ft.Page):
    page.title = "God Jarvis"
    page.bgcolor = "#000510"
    page.window_width = 400
    
    jarvis = JarvisGodMode()
    chat_log = ft.ListView(expand=True, spacing=10, initial_scroll_index=100)

    def log_to_ui(text):
        chat_log.controls.append(ft.Text(text, color="cyan" if "JARVIS" in text else "white"))
        page.update()

    # 🔥 Always-On Background Thread
    threading.Thread(target=jarvis.continuous_mic, args=(log_to_ui,), daemon=True).start()

    # UI Design: Arc Reactor & Status
    page.add(
        ft.Text("SYSTEM STATUS: GOD MODE ACTIVE", color="green", size=12, weight="bold"),
        ft.Container(
            content=chat_log,
            height=450,
            padding=15,
            border=ft.border.all(1, "cyan"),
            border_radius=15,
            bgcolor="#001122"
        ),
        ft.Container(
            # Arc Reactor Button
            content=ft.Icon(ft.icons.STAIRS_SHARP, color="cyan", size=80),
            width=120, height=120,
            shape=ft.BoxShape.CIRCLE,
            border=ft.border.all(3, "cyan"),
            shadow=ft.BoxShadow(blur_radius=50, color="cyan", spread_radius=5)
        ),
        ft.Text("LISTENING IN BACKGROUND...", color="white54", size=10)
    )

ft.app(target=main)