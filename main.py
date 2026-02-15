import flet as ft
import speech_recognition as sr
import threading
from plyer import tts

def main(page: ft.Page):
    page.title = "VEGA GOD MODE"
    page.bgcolor = "black"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- STATUS UI ---
    status_text = ft.Text("SYSTEM CHECK...", color="white", size=20)
    perm_icon = ft.Icon(ft.icons.LOCK, color="red", size=50)

    def speak(text):
        try:
            tts.speak(text)
        except:
            pass

    def check_permissions(e):
        # UI Update
        status_text.value = "SCANNING PERMISSIONS..."
        status_text.color = "cyan"
        page.update()
        
        # Fake loading to simulate system check
        speak("Checking system protocols.")
        
        # Visual Success
        perm_icon.icon = ft.icons.LOCK_OPEN
        perm_icon.color = "green"
        status_text.value = "ACCESS GRANTED: ALL FILES"
        status_text.color = "green"
        page.update()
        
        speak("Access Granted. I can now access all files and microphone.")

    # --- LAYOUT ---
    page.add(
        ft.Text("V E G A", size=40, weight="bold", color="purple"),
        ft.Container(height=20),
        perm_icon,
        status_text,
        ft.Container(height=40),
        ft.Text("Requires: Microphone & All Files Access", color="grey", size=12),
        ft.ElevatedButton(
            "GRANT FULL ACCESS", 
            on_click=check_permissions,
            bgcolor="purple", 
            color="white",
            icon=ft.icons.ADMIN_PANEL_SETTINGS
        )
    )

ft.app(target=main)
