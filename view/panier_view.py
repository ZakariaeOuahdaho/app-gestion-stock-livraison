import customtkinter as ctk
from tkinter import ttk, messagebox

class PanierWindow(ctk.CTkToplevel):
    def __init__(self, parent, panier):
        super().__init__(parent)
        self.panier = panier
        
        self.title("Mon Panier")
        self.geometry("600x400")

        # Configuration de la fenêtre
        self.setup_ui()
        self.update_panier()

    def setup_ui(self):
        # Titre
        self.label_title = ctk.CTkLabel(self, text="Mon Panier", font=("Arial", 20, "bold"))
        self.label_title.pack(pady=10)

        # Treeview pour les produits du panier
        columns = ("ID", "Nom", "Prix unitaire", "Quantité", "Total")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        # Configuration des colonnes
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Frame pour les boutons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill="x", padx=10, pady=5)

        # Label pour le total
        self.total_label = ctk.CTkLabel(self.button_frame, text="Total: 0.00 €")
        self.total_label.pack(side="left", padx=10)

        # Boutons
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

        self.btn_vider = ctk.CTkButton(
            self.button_frame,
            text="Vider le panier",
            command=self.vider_panier
        )
        self.btn_vider.pack(side="right", padx=5)

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
                f"{item['prix']:.2f} €",
                item['quantite'],
                f"{item['total']:.2f} €"
            ))

        # Mettre à jour le total
        total = self.panier.get_total()
        self.total_label.configure(text=f"Total: {total:.2f} €")

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

    def vider_panier(self):
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment vider le panier?"):
            self.panier.vider_panier()
            self.update_panier()