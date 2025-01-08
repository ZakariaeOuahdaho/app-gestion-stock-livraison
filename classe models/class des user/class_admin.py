from class_utilisateur import Utilisateur
class Admin(Utilisateur):
    def __init__(self, id=None, nom_utilisateur="", mot_de_passe=""):
        super().__init__(id, nom_utilisateur, mot_de_passe, role="admin")

    def initialize_data(self):
        self.load_products()
        self.update_stats()
        self.load_categories()
    
    def update_stats(self):
        self._get_total_revenue()
        self._get_order_count()
        self._get_products_sold()
    
    def _get_total_revenue(self):
        pass
    
    def _get_order_count(self):
        pass
    
    def _get_products_sold(self):
        pass

    def get_sales_by_category(self):
        pass
    
    def get_top_products(self):
        pass

    def load_products(self):
        pass
    
    def load_categories(self):
        pass
    
    def ajouter_produit(self, product_data):
        pass
    
    def modifier_produit(self, product_id, product_data):
        pass
    
    def supprimer_produit(self, product_id):
        pass