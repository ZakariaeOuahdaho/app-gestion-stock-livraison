import customtkinter as ctk
from tkinter import ttk, messagebox
from database.db import create_connection, close_connection
from mysql.connector import Error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ManagementPage(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Administration")
        self.geometry("1200x800")

        # Création des onglets
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=5)

        # Ajout des onglets
        self.tab_dashboard = self.tabview.add("Dashboard")
        self.tab_products = self.tabview.add("Gestion Produits")

        # Setup du dashboard
        self.setup_dashboard()

        # Setup de la gestion des produits
        self.setup_products_management()

        # Bouton déconnexion
        self.button_logout = ctk.CTkButton(self, text="Déconnexion", command=self.logout, fg_color="red")
        self.button_logout.pack(pady=10)

    def setup_dashboard(self):
        # Frame pour les statistiques
        stats_frame = ctk.CTkFrame(self.tab_dashboard)
        stats_frame.pack(fill="x", padx=10, pady=10)

        # Labels pour les statistiques
        self.stats_labels = {
            'revenue': ctk.CTkLabel(stats_frame, text="Revenu total: 0 MAD", font=("Arial", 16, "bold")),
            'orders': ctk.CTkLabel(stats_frame, text="Commandes: 0", font=("Arial", 16, "bold")),
            'products': ctk.CTkLabel(stats_frame, text="Produits vendus: 0", font=("Arial", 16, "bold"))
        }

        for label in self.stats_labels.values():
            label.pack(side="left", padx=20, pady=10)

        # Frame pour les graphiques
        self.graphs_frame = ctk.CTkFrame(self.tab_dashboard)
        self.graphs_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Création des graphiques
        self.create_graphs()

        # Bouton de rafraîchissement
        refresh_button = ctk.CTkButton(
            self.tab_dashboard,
            text="Rafraîchir",
            command=self.refresh_dashboard
        )
        refresh_button.pack(pady=10)

    def create_graphs(self):
        # Création d'une figure matplotlib avec 2 sous-graphiques
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Graphique des ventes par catégorie
        self.plot_sales_by_category(ax1)
        
        # Graphique des produits les plus vendus
        self.plot_top_products(ax2)

        # Intégration des graphiques dans l'interface
        canvas = FigureCanvasTkAgg(fig, self.graphs_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_sales_by_category(self, ax):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT c.nom, COUNT(cp.produit_id) as total_vendu
                    FROM categories c
                    LEFT JOIN produits p ON p.categorie_id = c.id
                    LEFT JOIN commande_produits cp ON cp.produit_id = p.id
                    GROUP BY c.nom
                """)
                results = cursor.fetchall()
                
                if results:
                    categories, values = zip(*results)
                    ax.pie(values, labels=categories, autopct='%1.1f%%')
                    ax.set_title('Ventes par catégorie')
                
            finally:
                cursor.close()
                close_connection(connection)

    def plot_top_products(self, ax):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT p.nom, SUM(cp.quantite) as total_vendu
                    FROM produits p
                    JOIN commande_produits cp ON cp.produit_id = p.id
                    GROUP BY p.id, p.nom
                    ORDER BY total_vendu DESC
                    LIMIT 5
                """)
                results = cursor.fetchall()
                
                if results:
                    products, values = zip(*results)
                    ax.bar(products, values)
                    ax.set_title('Top 5 des produits les plus vendus')
                    plt.xticks(rotation=45)
                
            finally:
                cursor.close()
                close_connection(connection)

    def update_stats(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Revenu total
                cursor.execute("SELECT SUM(total) FROM commandes")
                revenue = cursor.fetchone()[0] or 0
                self.stats_labels['revenue'].configure(
                    text=f"Revenu total: {revenue:.2f} €"
                )

                # Nombre de commandes
                cursor.execute("SELECT COUNT(*) FROM commandes")
                orders = cursor.fetchone()[0] or 0
                self.stats_labels['orders'].configure(
                    text=f"Commandes: {orders}"
                )

                # Produits vendus
                cursor.execute("SELECT SUM(quantite) FROM commande_produits")
                products = cursor.fetchone()[0] or 0
                self.stats_labels['products'].configure(
                    text=f"Produits vendus: {products}"
                )

            finally:
                cursor.close()
                close_connection(connection)

    def refresh_dashboard(self):
        self.update_stats()
        for widget in self.graphs_frame.winfo_children():
            widget.destroy()
        self.create_graphs()

    def setup_products_management(self):
        # Frame principale pour la gestion des produits
        main_frame = ctk.CTkFrame(self.tab_products)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Frame gauche pour l'ajout/modification de produits
        self.left_frame = ctk.CTkFrame(main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Frame droite pour la liste des produits
        self.right_frame = ctk.CTkFrame(main_frame)
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

        produit_id = self.tree.item(selected_item[0])['values'][0]
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

                # Modifier le produit
                cursor.execute("""
                    UPDATE produits 
                    SET nom = %s, description = %s, prix = %s, quantite = %s, categorie_id = %s
                    WHERE id = %s
                """, (nom, description, float(prix), int(quantite), categorie_id, produit_id))
                
                connection.commit()
                messagebox.showinfo("Succès", "Produit modifié avec succès")
                self.clear_form()
                self.load_products()
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors de la modification du produit: {e}")
            finally:
                cursor.close()
                close_connection(connection)

    def supprimer_produit(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit à supprimer")
            return

        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce produit ?"):
            produit_id = self.tree.item(selected_item[0])['values'][0]
            
            connection = create_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM produits WHERE id = %s", (produit_id,))
                    connection.commit()
                    messagebox.showinfo("Succès", "Produit supprimé avec succès")
                    self.clear_form()
                    self.load_products()
                except Error as e:
                    messagebox.showerror("Erreur", f"Erreur lors de la suppression du produit: {e}")
                finally:
                    cursor.close()
                    close_connection(connection)

    def logout(self):
        if messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter ?"):
            self.destroy()
            from view.login_view import LoginPage
            app = LoginPage()
            app.mainloop()

if __name__ == "__main__":
    app = ManagementPage()
    app.mainloop()