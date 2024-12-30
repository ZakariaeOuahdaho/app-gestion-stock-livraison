import customtkinter as ctk
from tkinter import messagebox
from mysql.connector import Error
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from database.db import create_connection, close_connection


class ClientPage (ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Espace Client")
        self.geometry("400x300")

        self.label_welcome = ctk.CTkLabel(self, text="Bienvenue dans votre espace client")
        self.label_welcome.pack(pady=20)

        self.button_logout = ctk.CTkButton(self, text="Déconnexion", command=self.logout)
        self.button_logout.pack(pady=20)

    def logout(self):
        from view.login_view import LoginPage 
        self.destroy()
        app = LoginPage()
        app.mainloop()