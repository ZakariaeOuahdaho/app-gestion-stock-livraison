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

        self.title("Admin Login")
        self.geometry("800x600")

        # Widgets de la page de connexion
        self.label_username = ctk.CTkLabel(self, text="Nom d'utilisateur")
        self.label_username.pack(pady=10)

        self.entry_username = ctk.CTkEntry(self)
        self.entry_username.pack(pady=5)

        self.label_password = ctk.CTkLabel(self, text="Mot de passe")
        self.label_password.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self, show="*")
        self.entry_password.pack(pady=5)

        self.button_login = ctk.CTkButton(self, text="Se connecter", command=self.login)
        self.button_login.pack(pady=20)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT * FROM utilisateurs WHERE nom_utilisateur=%s AND mot_de_passe=%s", 
                             (username, password))
                result = cursor.fetchone()
                if result:
                    self.open_management_page()
                else:
                    messagebox.showerror("Erreur", "Identifiants incorrects")
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur de la base de données: {e}")
            finally:
                cursor.close()
                close_connection(connection)
        else:
            messagebox.showerror("Erreur", "Impossible de se connecter à la base de données")

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
        self.destroy()
        app = AdminApp()
        app.mainloop()

if __name__ == "__main__":
    app = AdminApp()
    app.mainloop()