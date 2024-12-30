import customtkinter as ctk
from tkinter import messagebox
from mysql.connector import Error
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from database.db import create_connection, close_connection
from view.admin_view import ManagementPage
from view.client_view import ClientPage
from view.livreur_view import LivreurPage

class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login")
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
            cursor = connection.cursor(dictionary=True)  # Retourne les résultats sous forme de dictionnaire
            try:
                cursor.execute("""
                    SELECT * FROM utilisateurs 
                    WHERE nom_utilisateur = %s AND mot_de_passe = %s
                """, (username, password))
                
                user = cursor.fetchone()
                
                if user:
                    self.redirect_to_appropriate_page(user)
                else:
                    messagebox.showerror("Erreur", "Identifiants incorrects")
                    
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur de la base de données: {e}")
            finally:
                cursor.close()
                close_connection(connection)
        else:
            messagebox.showerror("Erreur", "Impossible de se connecter à la base de données")

    def redirect_to_appropriate_page(self, user):
        self.destroy()  # Ferme la page de login
        
        # Redirige vers la page appropriée selon le rôle
        if user['role'] == 'admin':
            app = ManagementPage()
        elif user['role'] == 'client':
            app = ClientPage()
        elif user['role'] == 'livreur':
            app = LivreurPage()
        else:
            messagebox.showerror("Erreur", "Rôle non reconnu")
            return
        
        app.mainloop()

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()
