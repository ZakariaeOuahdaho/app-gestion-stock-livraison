import customtkinter as ctk
from tkinter import ttk, messagebox
from database.db import create_connection, close_connection
from mysql.connector import Error
from models.panier import Panier

class ClientPage(ctk.CTk):
    def __init__(self, user_id=None):
        super().__init__()
        
        # Initialisation des variables utilisateur
        self.user_id = user_id
        self.panier = Panier(self.user_id)

        # Configuration de base de la fenêtre
        self.title("Espace Client")
        self.geometry("1200x700")
        self.configure(bg_color="#f0f0f0")

        # Configuration du grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Création des frames principales
        self.create_sidebar()
        self.create_main_content()
        
        # Chargement initial des données
        self.load_categories()
        self.load_products()
        self.update_cart_counter()

    def create_sidebar(self):
        # Frame de gauche pour les filtres et le panier
        self.sidebar = ctk.CTkFrame(self, width=250)
        self.sidebar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Titre du sidebar
        ctk.CTkLabel(
            self.sidebar,
            text="Menu Client",
            font=("Arial", 20, "bold")
        ).pack(pady=20)

        # Section Filtres
        self.create_filter_section()

        # Section Panier
        self.create_cart_section()

        # Bouton de déconnexion
        ctk.CTkButton(
            self.sidebar,
            text="Déconnexion",
            command=self.logout,
            fg_color="red",
            hover_color="darkred"
        ).pack(pady=20, padx=20, side="bottom")

    def create_filter_section(self):
        # Frame pour les filtres
        filter_frame = ctk.CTkFrame(self.sidebar)
        filter_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            filter_frame,
            text="Filtres",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Filtre par catégorie
        ctk.CTkLabel(
            filter_frame,
            text="Catégorie:"
        ).pack(pady=5)

        self.category_var = ctk.StringVar(value="Toutes les catégories")
        self.category_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=self.category_var,
            values=["Toutes les catégories"],
            command=self.filter_products
        )
        self.category_menu.pack(pady=5, padx=10, fill="x")

        # Filtre par prix
        ctk.CTkLabel(
            filter_frame,
            text="Prix maximum:"
        ).pack(pady=5)

        self.price_slider = ctk.CTkSlider(
            filter_frame,
            from_=0,
            to=1000,
            command=self.filter_products
        )
        self.price_slider.pack(pady=5, padx=10, fill="x")

        # Bouton réinitialiser les filtres
        ctk.CTkButton(
            filter_frame,
            text="Réinitialiser les filtres",
            command=self.reset_filters
        ).pack(pady=10)

    def create_cart_section(self):
        # Frame pour le panier
        cart_frame = ctk.CTkFrame(self.sidebar)
        cart_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            cart_frame,
            text="Mon Panier",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.cart_counter_label = ctk.CTkLabel(
            cart_frame,
            text="Articles: 0"
        )
        self.cart_counter_label.pack(pady=5)

        self.cart_total_label = ctk.CTkLabel(
            cart_frame,
            text="Total: 0.00 MAD"
        )
        self.cart_total_label.pack(pady=5)

        ctk.CTkButton(
            cart_frame,
            text="Voir le panier",
            command=self.show_cart
        ).pack(pady=10, fill="x", padx=10)

    def create_main_content(self):
        # Frame principal pour le contenu
        self.main_content = ctk.CTkFrame(self)
        self.main_content.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Barre de recherche
        self.create_search_bar()

        # Liste des produits
        self.create_product_list()

    def create_search_bar(self):
        # Frame pour la recherche
        search_frame = ctk.CTkFrame(self.main_content)
        search_frame.pack(fill="x", padx=10, pady=10)

        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Rechercher un produit...",
            textvariable=self.search_var,
            width=300
        )
        search_entry.pack(side="left", padx=5)

        ctk.CTkButton(
            search_frame,
            text="Rechercher",
            command=self.search_products
        ).pack(side="left", padx=5)

    def create_product_list(self):
        # Frame pour la liste des produits
        list_frame = ctk.CTkFrame(self.main_content)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Création du Treeview
        columns = ("ID", "Nom", "Description", "Prix", "Stock", "Catégorie")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")

        # Configuration des colonnes
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nom", text="Nom du produit")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Prix", text="Prix")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Catégorie", text="Catégorie")

        self.tree.column("ID", width=50)
        self.tree.column("Nom", width=200)
        self.tree.column("Description", width=300)
        self.tree.column("Prix", width=100)
        self.tree.column("Stock", width=100)
        self.tree.column("Catégorie", width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bouton d'ajout au panier
        ctk.CTkButton(
            self.main_content,
            text="Ajouter au panier",
            command=self.add_to_cart
        ).pack(pady=10)

    def load_categories(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT nom FROM categories")
                categories = ["Toutes les catégories"] + [row[0] for row in cursor.fetchall()]
                self.category_menu.configure(values=categories)
            except Error as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement des catégories: {e}")
            finally:
                cursor.close()
                close_connection(connection)

    def load_products(self, category=None, search_term=None, max_price=None):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                query = """
                    SELECT p.id, p.nom, p.description, p.prix, p.quantite, c.nom 
                    FROM produits p 
                    LEFT JOIN categories c ON p.categorie_id = c.id
                    WHERE 1=1
                """
                params = []

                if category and category != "Toutes les catégories":
                    query += " AND c.nom = %s"
                    params.append(category)

                if search_term:
                    query += " AND p.nom LIKE %s"
                    params.append(f"%{search_term}%")

                if max_price:
                    query += " AND p.prix <= %s"
                    params.append(max_price)

                cursor.execute(query, params)

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

    def filter_products(self, *args):
        category = self.category_var.get()
        max_price = self.price_slider.get()
        search_term = self.search_var.get()
        self.load_products(category, search_term, max_price)

    def search_products(self):
        self.filter_products()

    def reset_filters(self):
        self.category_var.set("Toutes les catégories")
        self.price_slider.set(1000)
        self.search_var.set("")
        self.load_products()

    def add_to_cart(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un produit")
            return

        item = self.tree.item(selected_item[0])
        produit_id = item['values'][0]
        stock_disponible = item['values'][4]

        # Demander la quantité
        dialog = ctk.CTkInputDialog(
            text=f"Entrez la quantité désirée (max {stock_disponible}):",
            title="Ajouter au panier"
        )
        quantite = dialog.get_input()

        if quantite and quantite.isdigit():
            quantite = int(quantite)
            if 0 < quantite <= stock_disponible:
                if self.panier.ajouter_produit(produit_id, quantite):
                    messagebox.showinfo("Succès", "Produit ajouté au panier")
                    self.update_cart_counter()
                else:
                    messagebox.showerror("Erreur", "Erreur lors de l'ajout au panier")
            else:
                messagebox.showerror("Erreur", "Quantité invalide")

    def show_cart(self):
        from view.panier_view import PanierWindow
        panier_window = PanierWindow(self, self.panier)
        panier_window.grab_set()

    def update_cart_counter(self):
        total_items = sum(self.panier.items.values())
        total_price = self.panier.get_total()
        self.cart_counter_label.configure(text=f"Articles: {total_items}")
        self.cart_total_label.configure(text=f"Total: {total_price:.2f} MAD")

    def logout(self):
        if messagebox.askyesno("Déconnexion", "Voulez-vous vraiment vous déconnecter ?"):
            self.destroy()
            from view.login_view import LoginPage
            app = LoginPage()
            app.mainloop()

if __name__ == "__main__":
    app = ClientPage(user_id=2)  # Pour les tests
    app.mainloop()