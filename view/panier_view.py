import customtkinter as ctk
from tkinter import ttk, messagebox
from database.db import create_connection, close_connection

class PanierWindow(ctk.CTkToplevel):
    def __init__(self, parent, panier):
        super().__init__(parent)
        
        self.title("Mon Panier")
        self.geometry("600x500")  # Augmenté la hauteur pour le bouton
        
        self.panier = panier
        
        # Configuration de la fenêtre
        self.setup_ui()
        self.update_panier()

    def setup_ui(self):
        # Titre
        self.label_title = ctk.CTkLabel(
            self, 
            text="Mon Panier", 
            font=("Arial", 20, "bold")
        )
        self.label_title.pack(pady=10)

        # Treeview pour les produits du panier
        columns = ("ID", "Nom", "Prix unitaire", "Quantité", "Total")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        # Configuration des colonnes
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Frame pour les boutons d'action
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill="x", padx=10, pady=5)

        # Label pour le total
        self.total_label = ctk.CTkLabel(
            self.button_frame, 
            text="Total: 0.00 MAD",
            font=("Arial", 16, "bold")
        )
        self.total_label.pack(side="left", padx=10)

        # Boutons d'action
        self.btn_supprimer = ctk.CTkButton(
            self.button_frame,
            text="Supprimer",
            command=self.supprimer_selection
        )
        self.btn_supprimer.pack(side="right", padx=5)

        self.btn_modifier = ctk.CTkButton(
            self.button_frame,
            text="Modifier quantité",
            command=self.modifier_quantite
        )
        self.btn_modifier.pack(side="right", padx=5)

        # Frame pour le bouton de confirmation
        self.confirm_frame = ctk.CTkFrame(self)
        self.confirm_frame.pack(fill="x", padx=10, pady=10)

        # Bouton de confirmation du panier
        self.btn_confirmer = ctk.CTkButton(
            self.confirm_frame,
            text="Confirmer la commande",
            font=("Arial", 14, "bold"),
            height=40,
            command=self.confirmer_commande,
            fg_color="green",
            hover_color="dark green"
        )
        self.btn_confirmer.pack(pady=10, padx=20, fill="x")

    def update_panier(self):
        # Effacer les anciennes données
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Charger les nouveaux produits
        contenu = self.panier.get_contenu_panier()
        for item in contenu:
            self.tree.insert("", "end", values=(
                item['id'],
                item['nom'],
                f"{item['prix']:.2f} MAD",
                item['quantite'],
                f"{item['total']:.2f} MAD"
            ))

        # Mettre à jour le total
        total = self.panier.get_total()
        self.total_label.configure(text=f"Total: {total:.2f} MAD")

    def supprimer_selection(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit")
            return

        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce produit du panier?"):
            item = self.tree.item(selection[0])
            produit_id = item['values'][0]
            self.panier.supprimer_produit(produit_id)
            self.update_panier()

    def modifier_quantite(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit")
            return

        item = self.tree.item(selection[0])
        produit_id = item['values'][0]
        quantite_actuelle = item['values'][3]

        # Créer une fenêtre de dialogue pour la nouvelle quantité
        dialog = ctk.CTkInputDialog(
            text="Entrez la nouvelle quantité:",
            title="Modifier la quantité"
        )
        nouvelle_quantite = dialog.get_input()

        if nouvelle_quantite and nouvelle_quantite.isdigit():
            nouvelle_quantite = int(nouvelle_quantite)
            if nouvelle_quantite > 0:
                self.panier.modifier_quantite(produit_id, nouvelle_quantite)
                self.update_panier()
            else:
                messagebox.showerror("Erreur", "La quantité doit être supérieure à 0")

    def confirmer_commande(self):
        if not self.tree.get_children():
            messagebox.showwarning("Attention", "Votre panier est vide")
            return

        if messagebox.askyesno("Confirmation", "Voulez-vous confirmer votre commande?"):
            # Ouvrir la fenêtre de confirmation de commande
            from view.confirmation_commande import ConfirmationCommande
            confirmation = ConfirmationCommande(self, self.panier, self.panier.utilisateur_id)
            confirmation.grab_set()
            self.withdraw()  # Cache la fenêtre du panier

    def on_closing(self):
        self.destroy()
        if hasattr(self, 'parent'):
            self.parent.update_cart_counter()