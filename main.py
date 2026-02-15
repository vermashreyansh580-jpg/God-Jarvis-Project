import flet as ft
import speech_recognition as sr
import pyttsx3
import threading
import requests
import os
import shutil

# --- CONFIG ---
GROQ_API_KEY = "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"

class JarvisBrain:
    def __init__(self, page):
        self.page = page
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        # Android Root Path
        self.root_path = "/storage/emulated/0/" 

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    # --- FILE SYSTEM POWERS ---
    def find_file(self, filename):
        results = []
        # Searching primarily in Documents/Downloads to save time
        search_dirs = [
            os.path.join(self.root_path, "Download"),
            os.path.join(self.root_path, "Documents"),
            os.path.join(self.root_path, "DCIM")
        ]
        for folder in search_dirs:
            for root, dirs, files in os.walk(folder):
                if filename.lower() in [f.lower() for f in files]:
                    results.append(os.path.join(root, filename))
        return results[0] if results else None

    def delete_file(self, filepath):
        try:
            os.remove(filepath)
            return "File deleted successfully."
        except: return "Permission denied or file not found."

    def create_folder(self, folder_name):
        path = os.path.join(self.root_path, folder_name)
        os.makedirs(path, exist_ok=True)
        return f"Folder {folder_name} created."

    # --- BRAIN & LISTENER ---
    def listen_loop(self, chat_callback):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                try:
                    audio = self.recognizer.listen(source, phrase_time_limit=5)
                    # "hi-IN" helps capture Hindi/English mix better
                    text = self.recognizer.recognize_google(audio, language="hi-IN").lower()
                    
                    if "jarvis" in text:
                        clean_text = text.replace("jarvis", "").strip()
                        chat_callback(f"YOU: {clean_text}", True)
                        
                        response = self.ask_ai(clean_text)
                        
                        # EXECUTE FILE ACTIONS
                        if "ACTION:SEARCH:" in response:
                            fname = response.split(":")[2]
                            path = self.find_file(fname)
                            reply = f"Found it at: {path}" if path else "File not found."
                            chat_callback(f"JARVIS: {reply}", False)
                            self.speak(reply)
                        
                        elif "ACTION:DELETE:" in response:
                            path = response.split(":")[2]
                            status = self.delete_file(path)
                            chat_callback(f"JARVIS: {status}", False)
                            self.speak(status)
                            
                        else:
                            chat_callback(f"JARVIS: {response}", False)
                            self.speak(response)
                except: pass

    def ask_ai(self, prompt):
        # SYSTEM PROMPT FOR MULTILINGUAL & FILES
        sys_msg = """
        You are God Jarvis. 
        1. LANGUAGE: Detect user language (Hindi/English) and reply in the SAME language.
        2. FILES: If user asks to find a file, reply ONLY: ACTION:SEARCH:filename.ext
        3. DELETE: If user asks to delete, reply ONLY: ACTION:DELETE:filepath
        4. GENERAL: Be helpful and concise.
        """
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "system", "content": sys_msg},
                         {"role": "user", "content": prompt}]
        }
        try:
            return requests.post(url, headers=headers, json=data).json()['choices'][0]['message']['content']
        except: return "Server Error."

def main(page: ft.Page):
    page.title = "Jarvis FileManager"
    page.bgcolor = "#000510"
    page.theme_mode = ft.ThemeMode.DARK
    
    brain = JarvisBrain(page)
    chat_list = ft.ListView(expand=True, spacing=10, padding=20)

    def add_msg(text, is_user):
        align = ft.MainAxisAlignment.END if is_user else ft.MainAxisAlignment.START
        color = "cyan" if not is_user else "white"
        chat_list.controls.append(ft.Row([ft.Text(text, color=color, weight="bold")], alignment=align))
        page.update()

    threading.Thread(target=brain.listen_loop, args=(add_msg,), daemon=True).start()

    page.add(
        ft.AppBar(title=ft.Text("JARVIS FILE GOD"), bgcolor="#001F3F"),
        ft.Container(content=chat_list, expand=True, border=ft.border.all(1, "cyan"), border_radius=10, margin=10),
        ft.Text("ACCESS: ALL FILES | LANG: MULTI", color="green", size=10, text_align="center")
    )

ft.app(target=main)
