import customtkinter as ctk
from tkinter import messagebox

# Configuration de base pour CustomTkinter
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class AdminApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Admin Login")
        self.geometry("300x200")

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

        # Remplacez cette vérification par une vérification réelle de la base de données
        if username == "admin" and password == "password":
            self.open_management_page()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")

    def open_management_page(self):
        # Fermer la fenêtre de connexion
        self.destroy()

        # Ouvrir la page de gestion
        management_page = ManagementPage()
        management_page.mainloop()

class ManagementPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Page de Gestion")
        self.geometry("400x300")

        self.label_welcome = ctk.CTkLabel(self, text="Bienvenue sur la page de gestion")
        self.label_welcome.pack(pady=20)

        # Ajoutez ici d'autres widgets pour la gestion des produits, commandes, etc.
        self.button_logout = ctk.CTkButton(self, text="Déconnexion", command=self.logout)
        self.button_logout.pack(pady=20)

    def logout(self):
        self.destroy()
        app = AdminApp()
        app.mainloop()

if __name__ == "__main__":
    app = AdminApp()
    app.mainloop()