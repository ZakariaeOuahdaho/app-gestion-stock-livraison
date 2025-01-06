import customtkinter as ctk
from tkinter import messagebox
from database.db import create_connection, close_connection

class ConfirmationCommande(ctk.CTkToplevel):
    def __init__(self, parent, panier, user_id):
        super().__init__(parent)
        
        self.title("Confirmation de commande")
        self.geometry("600x700")
        
        self.panier = panier
        self.user_id = user_id
        self.mode_livraison = ctk.StringVar(value="retrait")
        
        self.setup_ui()

    def setup_ui(self):
        # Titre
        ctk.CTkLabel(
            self,
            text="Confirmation de votre commande",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        # Récapitulatif du panier
        self.create_recap_frame()

        # Mode de livraison
        self.create_delivery_frame()

        # Bouton de confirmation final
        ctk.CTkButton(
            self,
            text="Confirmer et payer",
            command=self.finaliser_commande,
            fg_color="green",
            hover_color="dark green"
        ).pack(pady=20, padx=20)

    def create_recap_frame(self):
        recap_frame = ctk.CTkFrame(self)
        recap_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            recap_frame,
            text="Récapitulatif de votre commande",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Afficher les produits
        contenu = self.panier.get_contenu_panier()
        for item in contenu:
            ctk.CTkLabel(
                recap_frame,
                text=f"{item['nom']} x{item['quantite']} = {item['total']}€"
            ).pack(pady=2)

        # Total
        total = self.panier.get_total()
        ctk.CTkLabel(
            recap_frame,
            text=f"Total: {total}€",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

    def create_delivery_frame(self):
        delivery_frame = ctk.CTkFrame(self)
        delivery_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            delivery_frame,
            text="Mode de livraison",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Options de livraison
        ctk.CTkRadioButton(
            delivery_frame,
            text="Retrait en magasin",
            variable=self.mode_livraison,
            value="retrait",
            command=self.toggle_adresse
        ).pack(pady=5)

        ctk.CTkRadioButton(
            delivery_frame,
            text="Livraison à domicile",
            variable=self.mode_livraison,
            value="livraison",
            command=self.toggle_adresse
        ).pack(pady=5)

        # Frame pour l'adresse
        self.adresse_frame = ctk.CTkFrame(delivery_frame)
        self.adresse_frame.pack(fill="x", pady=10)
        self.adresse_frame.pack_forget()

        ctk.CTkLabel(
            self.adresse_frame,
            text="Adresse de livraison:"
        ).pack(pady=5)

        self.adresse_entry = ctk.CTkEntry(
            self.adresse_frame,
            width=300,
            placeholder_text="Entrez votre adresse complète"
        )
        self.adresse_entry.pack(pady=5)

    def toggle_adresse(self):
        if self.mode_livraison.get() == "livraison":
            self.adresse_frame.pack(fill="x", pady=10)
        else:
            self.adresse_frame.pack_forget()

    def finaliser_commande(self):
        if self.mode_livraison.get() == "livraison" and not self.adresse_entry.get():
            messagebox.showwarning("Attention", "Veuillez entrer une adresse de livraison")
            return

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Créer la commande
                total = self.panier.get_total()
                cursor.execute("""
                    INSERT INTO commandes (utilisateur_id, total, statut)
                    VALUES (%s, %s, 'En attente')
                """, (self.user_id, total))
                
                commande_id = cursor.lastrowid

                # Ajouter les produits de la commande
                contenu = self.panier.get_contenu_panier()
                for item in contenu:
                    cursor.execute("""
                        INSERT INTO commande_produits 
                        (commande_id, produit_id, quantite, prix_unitaire)
                        VALUES (%s, %s, %s, %s)
                    """, (commande_id, item['id'], item['quantite'], item['prix']))

                # Si livraison, créer une entrée dans la table livraisons
                if self.mode_livraison.get() == "livraison":
                    cursor.execute("""
                        INSERT INTO livraisons 
                        (commande_id, adresse_livraison, statut)
                        VALUES (%s, %s, 'En attente')
                    """, (commande_id, self.adresse_entry.get()))

                connection.commit()
                
                # Vider le panier
                self.panier.vider_panier()
                
                messagebox.showinfo("Succès", 
                    "Commande confirmée avec succès!\n" + 
                    ("Votre commande sera livrée à l'adresse indiquée." if self.mode_livraison.get() == "livraison" 
                     else "Vous pouvez retirer votre commande en magasin.")
                )
                self.destroy()
                self.master.destroy()  # Ferme aussi la fenêtre du panier

            except Exception as e:
                connection.rollback()
                messagebox.showerror("Erreur", f"Erreur lors de la confirmation: {str(e)}")
            finally:
                cursor.close()
                close_connection(connection)