import customtkinter as ctk
from tkinter import ttk, messagebox
from mysql.connector import Error
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from database.db import create_connection, close_connection

class LivreurPage(ctk.CTk):
    def __init__(self, user_id):
        super().__init__()
        
        self.user_id = user_id
        
        # Configuration de base de la fenêtre
        self.title("Espace Livreur")
        self.geometry("1200x700")
        
        # Configuration du grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Création des frames principales
        self.create_sidebar()
        self.create_main_content()
        
        # Chargement initial des livraisons
        self.load_deliveries()

    def create_sidebar(self):
        # Frame de gauche
        self.sidebar = ctk.CTkFrame(self, width=250)
        self.sidebar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Titre
        ctk.CTkLabel(
            self.sidebar,
            text="Menu Livreur",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        # Filtres de statut
        self.create_status_filters()

        # Statistiques
        self.create_stats_section()

        # Bouton de déconnexion
        ctk.CTkButton(
            self.sidebar,
            text="Déconnexion",
            command=self.logout,
            fg_color="red",
            hover_color="darkred"
        ).pack(pady=20, padx=20, side="bottom")

    def create_status_filters(self):
        filter_frame = ctk.CTkFrame(self.sidebar)
        filter_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            filter_frame,
            text="Filtrer par statut",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.status_var = ctk.StringVar(value="Toutes")
        statuses = ["Toutes", "En attente", "En cours", "Livrée"]
        
        for status in statuses:
            ctk.CTkRadioButton(
                filter_frame,
                text=status,
                variable=self.status_var,
                value=status,
                command=self.filter_deliveries
            ).pack(pady=5)

    def create_stats_section(self):
        stats_frame = ctk.CTkFrame(self.sidebar)
        stats_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            stats_frame,
            text="Statistiques",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.stats_labels = {
            'total': ctk.CTkLabel(stats_frame, text="Total livraisons: 0"),
            'pending': ctk.CTkLabel(stats_frame, text="En attente: 0"),
            'in_progress': ctk.CTkLabel(stats_frame, text="En cours: 0"),
            'completed': ctk.CTkLabel(stats_frame, text="Terminées: 0")
        }

        for label in self.stats_labels.values():
            label.pack(pady=5)

    def create_main_content(self):
        # Frame principal
        self.main_content = ctk.CTkFrame(self)
        self.main_content.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Titre
        ctk.CTkLabel(
            self.main_content,
            text="Gestion des Livraisons",
            font=("Arial", 24, "bold")
        ).pack(pady=10)

        # Création du Treeview pour les livraisons
        self.create_delivery_list()

        # Boutons d'action
        self.create_action_buttons()

    def create_delivery_list(self):
        # Frame pour la liste
        list_frame = ctk.CTkFrame(self.main_content)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview
        columns = ("ID", "Client", "Adresse", "Date", "Statut", "Total")
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # Configuration des colonnes
        self.tree.heading("ID", text="ID")
        self.tree.heading("Client", text="Client")
        self.tree.heading("Adresse", text="Adresse de livraison")
        self.tree.heading("Date", text="Date commande")
        self.tree.heading("Statut", text="Statut")
        self.tree.heading("Total", text="Total")

        self.tree.column("ID", width=50)
        self.tree.column("Client", width=150)
        self.tree.column("Adresse", width=300)
        self.tree.column("Date", width=150)
        self.tree.column("Statut", width=100)
        self.tree.column("Total", width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_action_buttons(self):
        button_frame = ctk.CTkFrame(self.main_content)
        button_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(
            button_frame,
            text="Prendre en charge",
            command=self.take_delivery
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Marquer comme livrée",
            command=self.complete_delivery
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="Voir détails",
            command=self.show_delivery_details
        ).pack(side="left", padx=5)

    def load_deliveries(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                status_filter = self.status_var.get()
                query = """
                    SELECT l.id, u.nom_utilisateur, l.adresse_livraison, 
                           c.date_commande, l.statut, c.total
                    FROM livraisons l
                    JOIN commandes c ON l.commande_id = c.id
                    JOIN utilisateurs u ON c.utilisateur_id = u.id
                    WHERE l.livreur_id IS NULL OR l.livreur_id = %s
                """
                
                if status_filter != "Toutes":
                    query += " AND l.statut = %s"
                    cursor.execute(query, (self.user_id, status_filter))
                else:
                    cursor.execute(query, (self.user_id,))

                # Effacer les anciennes données
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Insérer les nouvelles données
                for row in cursor.fetchall():
                    self.tree.insert("", "end", values=row)

                # Mettre à jour les statistiques
                self.update_statistics()

            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement des livraisons: {e}")
            finally:
                cursor.close()
                close_connection(connection)

    def update_statistics(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Total des livraisons
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM livraisons 
                    WHERE livreur_id IS NULL OR livreur_id = %s
                """, (self.user_id,))
                total = cursor.fetchone()[0]
                self.stats_labels['total'].configure(text=f"Total livraisons: {total}")

                # Livraisons par statut
                statuses = {
                    'pending': 'En attente',
                    'in_progress': 'En cours',
                    'completed': 'Livrée'
                }
                
                for key, status in statuses.items():
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM livraisons 
                        WHERE (livreur_id IS NULL OR livreur_id = %s)
                        AND statut = %s
                    """, (self.user_id, status))
                    count = cursor.fetchone()[0]
                    self.stats_labels[key].configure(text=f"{status}: {count}")

            finally:
                cursor.close()
                close_connection(connection)

    def filter_deliveries(self):
        self.load_deliveries()

    def take_delivery(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner une livraison")
            return

        delivery_id = self.tree.item(selected_item[0])['values'][0]
        
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE livraisons 
                    SET statut = 'En cours', livreur_id = %s 
                    WHERE id = %s AND statut = 'En attente'
                """, (self.user_id, delivery_id))
                
                connection.commit()
                
                if cursor.rowcount > 0:
                    messagebox.showinfo("Succès", "Livraison prise en charge")
                    self.load_deliveries()
                else:
                    messagebox.showwarning("Attention", "Cette livraison ne peut pas être prise en charge")

            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la mise à jour: {e}")
            finally:
                cursor.close()
                close_connection(connection)

    def complete_delivery(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner une livraison")
            return

        delivery_id = self.tree.item(selected_item[0])['values'][0]
        
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE livraisons 
                    SET statut = 'Livrée', date_livraison = CURRENT_TIMESTAMP 
                    WHERE id = %s AND statut = 'En cours' AND livreur_id = %s
                """, (delivery_id, self.user_id))
                
                connection.commit()
                
                if cursor.rowcount > 0:
                    messagebox.showinfo("Succès", "Livraison marquée comme terminée")
                    self.load_deliveries()
                else:
                    messagebox.showwarning("Attention", "Cette livraison ne peut pas être marquée comme terminée")

            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la mise à jour: {e}")
            finally:
                cursor.close()
                close_connection(connection)

    def show_delivery_details(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner une livraison")
            return

        delivery_id = self.tree.item(selected_item[0])['values'][0]
        DeliveryDetailsWindow(self, delivery_id)

    def logout(self):
        if messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter ?"):
            self.destroy()
            from view.login_view import LoginPage
            app = LoginPage()
            app.mainloop()

class DeliveryDetailsWindow(ctk.CTkToplevel):
    def __init__(self, parent, delivery_id):
        super().__init__(parent)
        
        self.title("Détails de la livraison")
        self.geometry("600x400")
        
        self.delivery_id = delivery_id
        self.load_delivery_details()

    def load_delivery_details(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                
                # Charger les détails de la livraison
                cursor.execute("""
                    SELECT l.*, u.nom_utilisateur, c.date_commande, c.total
                    FROM livraisons l
                    JOIN commandes c ON l.commande_id = c.id
                    JOIN utilisateurs u ON c.utilisateur_id = u.id
                    WHERE l.id = %s
                """, (self.delivery_id,))
                
                delivery = cursor.fetchone()
                
                if delivery:
                    self.display_delivery_details(delivery)
                    
                    # Charger les produits de la commande
                    cursor.execute("""
                        SELECT p.nom, cp.quantite, cp.prix_unitaire
                        FROM commande_produits cp
                        JOIN produits p ON cp.produit_id = p.id
                        WHERE cp.commande_id = %s
                    """, (delivery['commande_id'],))
                    
                    products = cursor.fetchall()
                    self.display_products(products)
                
            finally:
                cursor.close()
                close_connection(connection)

    def display_delivery_details(self, delivery):
        # Afficher les détails de la livraison
        details_frame = ctk.CTkFrame(self)
        details_frame.pack(fill="x", padx=10, pady=10)

        labels = [
            f"Client: {delivery['nom_utilisateur']}",
            f"Adresse: {delivery['adresse_livraison']}",
            f"Date: {delivery['date_commande']}",
            f"Statut: {delivery['statut']}",
            f"Total: {delivery['total']}€"
        ]

        for label in labels:
            ctk.CTkLabel(details_frame, text=label).pack(pady=5)

    def display_products(self, products):
        # Afficher la liste des produits
        products_frame = ctk.CTkFrame(self)
        products_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            products_frame,
            text="Produits commandés",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Treeview pour les produits
        columns = ("Produit", "Quantité", "Prix unitaire", "Total")
        tree = ttk.Treeview(products_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for product in products:
            total = product['prix_unitaire'] * product['quantite']
            tree.insert("", "end", values=(
                product['nom'],
                product['quantite'],
                f"{product['prix_unitaire']}€",
                f"{total}€"
            ))

        tree.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = LivreurPage(user_id=1)  # Pour les tests
    app.mainloop()