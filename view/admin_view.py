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



import customtkinter as ctk
from tkinter import ttk, messagebox
from database.db import create_connection, close_connection
from mysql.connector import Error

class ManagementPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestion des Produits")
        self.geometry("800x600")

        # Frame principale
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Frame gauche pour l'ajout/modification de produits
        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Frame droite pour la liste des produits
        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        self.setup_product_form()
        self.setup_product_list()
        self.load_products()

    def setup_product_form(self):
        # Titre
        ctk.CTkLabel(self.left_frame, text="Ajouter/Modifier un Produit", font=("Arial", 16, "bold")).pack(pady=10)

        # Champs de formulaire
        self.nom_var = ctk.StringVar()
        ctk.CTkLabel(self.left_frame, text="Nom du produit:").pack(pady=5)
        self.nom_entry = ctk.CTkEntry(self.left_frame, textvariable=self.nom_var)
        self.nom_entry.pack(pady=5)

        self.description_var = ctk.StringVar()
        ctk.CTkLabel(self.left_frame, text="Description:").pack(pady=5)
        self.description_entry = ctk.CTkEntry(self.left_frame, textvariable=self.description_var)
        self.description_entry.pack(pady=5)

        self.prix_var = ctk.StringVar()
        ctk.CTkLabel(self.left_frame, text="Prix:").pack(pady=5)
        self.prix_entry = ctk.CTkEntry(self.left_frame, textvariable=self.prix_var)
        self.prix_entry.pack(pady=5)

        self.quantite_var = ctk.StringVar()
        ctk.CTkLabel(self.left_frame, text="Quantité:").pack(pady=5)
        self.quantite_entry = ctk.CTkEntry(self.left_frame, textvariable=self.quantite_var)
        self.quantite_entry.pack(pady=5)

        # Combobox pour les catégories
        ctk.CTkLabel(self.left_frame, text="Catégorie:").pack(pady=5)
        self.categorie_combobox = ttk.Combobox(self.left_frame)
        self.categorie_combobox.pack(pady=5)
        self.load_categories()

        # Boutons
        self.btn_ajouter = ctk.CTkButton(self.left_frame, text="Ajouter", command=self.ajouter_produit)
        self.btn_ajouter.pack(pady=10)

        self.btn_modifier = ctk.CTkButton(self.left_frame, text="Modifier", command=self.modifier_produit)
        self.btn_modifier.pack(pady=5)

        self.btn_supprimer = ctk.CTkButton(self.left_frame, text="Supprimer", command=self.supprimer_produit)
        self.btn_supprimer.pack(pady=5)

    def setup_product_list(self):
        # Titre
        ctk.CTkLabel(self.right_frame, text="Liste des Produits", font=("Arial", 16, "bold")).pack(pady=10)

        # Treeview pour la liste des produits
        columns = ("ID", "Nom", "Prix", "Quantité", "Catégorie")
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show="headings")
        
        # Définir les en-têtes
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(pady=10, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.item_selected)

    def load_categories(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT nom FROM categories")
                categories = [row[0] for row in cursor.fetchall()]
                self.categorie_combobox['values'] = categories
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement des catégories: {e}")
            finally:
                cursor.close()
                close_connection(connection)

    def load_products(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT p.id, p.nom, p.prix, p.quantite, c.nom 
                    FROM produits p 
                    LEFT JOIN categories c ON p.categorie_id = c.id
                """)
                # Effacer les anciennes données
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Insérer les nouvelles données
                for row in cursor.fetchall():
                    self.tree.insert("", "end", values=row)
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement des produits: {e}")
            finally:
                cursor.close()
                close_connection(connection)

    def ajouter_produit(self):
        nom = self.nom_var.get()
        description = self.description_var.get()
        prix = self.prix_var.get()
        quantite = self.quantite_var.get()
        categorie = self.categorie_combobox.get()

        if not all([nom, prix, quantite, categorie]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires")
            return

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                # Obtenir l'ID de la catégorie
                cursor.execute("SELECT id FROM categories WHERE nom = %s", (categorie,))
                categorie_id = cursor.fetchone()[0]

                # Insérer le produit
                cursor.execute("""
                    INSERT INTO produits (nom, description, prix, quantite, categorie_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nom, description, float(prix), int(quantite), categorie_id))
                
                connection.commit()
                messagebox.showinfo("Succès", "Produit ajouté avec succès")
                self.clear_form()
                self.load_products()
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout du produit: {e}")
            finally:
                cursor.close()
                close_connection(connection)

    def clear_form(self):
        self.nom_var.set("")
        self.description_var.set("")
        self.prix_var.set("")
        self.quantite_var.set("")
        self.categorie_combobox.set("")

    def item_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            values = item['values']
            # Remplir le formulaire avec les valeurs sélectionnées
            self.nom_var.set(values[1])
            self.prix_var.set(values[2])
            self.quantite_var.set(values[3])
            self.categorie_combobox.set(values[4])

    def modifier_produit(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit à modifier")
            return

        # Code pour modifier le produit...

    def supprimer_produit(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit à supprimer")
            return

        # Code pour supprimer le produit...