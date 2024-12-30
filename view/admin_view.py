import customtkinter as ctk
from tkinter import messagebox
from mysql.connector import Error
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from database.db import create_connection, close_connection

# Configuration de base pour CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AdminApp(ctk.CTk):
    def __init__(self):
        super().__init__()
    def open_management_page(self):
        self.destroy()
        management_page = ManagementPage()
        management_page.mainloop()

class ManagementPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Page de Gestion")
        self.geometry("800x600")

        self.label_welcome = ctk.CTkLabel(self, text="Bienvenue sur la page de gestion")
        self.label_welcome.pack(pady=20)

        self.button_logout = ctk.CTkButton(self, text="Déconnexion", command=self.logout)
        self.button_logout.pack(pady=20)

    def logout(self):
        from view.login_view import LoginPage
        self.destroy()
        app = LoginPage()
        app.mainloop()

if __name__ == "__main__":
    app = AdminApp()
    app.mainloop()