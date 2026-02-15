import flet as ft
import time

def main(page: ft.Page):
    page.title = "VEGA AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 1. UI Elements (Minimal and Safe)
    status_icon = ft.Icon(ft.icons.SHIELD_LOCK, color="red", size=50)
    status_text = ft.Text("WAITING FOR PERMISSIONS...", color="red")
    chat_box = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=300)

    # 2. Permission Checker Logic
    def check_and_start(e=None):
        # Yahan hum Android se permissions ki 'demand' karenge
        status_text.value = "INITIALIZING CORE..."
        status_text.color = "cyan"
        status_icon.icon = ft.icons.SATELLITE_ALT
        status_icon.color = "cyan"
        page.update()
        
        time.sleep(2) # System ko load hone ka time dena
        
        # Ab chat box activate karenge
        chat_box.controls.append(ft.Text("VEGA: Systems Online, Shreyansh.", color="purple"))
        status_text.value = "VEGA IS LIVE"
        status_icon.icon = ft.icons.RADIO_BUTTON_CHECKED
        status_icon.color = "green"
        page.update()

    # Futuristic UI Layout
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("V E G A", size=40, weight="bold", color="cyan", letter_spacing=10),
                ft.Divider(color="white24"),
                status_icon,
                status_text,
                ft.Container(height=20),
                ft.Container(
                    content=chat_box,
                    padding=10,
                    border=ft.border.all(1, "cyan"),
                    border_radius=10,
                    bgcolor="#111111"
                ),
                ft.ElevatedButton(
                    "GRANT ALL ACCESS", 
                    icon=ft.icons.KEY, 
                    on_click=check_and_start,
                    bgcolor="cyan",
                    color="black"
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            border_radius=20,
            border=ft.border.all(2, "cyan")
        )
    )

ft.app(target=main)
