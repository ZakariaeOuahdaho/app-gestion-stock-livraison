from class_utilisateur import Utilisateur
class Client(Utilisateur):
    def __init__(self, id=None, nom_utilisateur="", mot_de_passe=""):
        super().__init__(id, nom_utilisateur, mot_de_passe, role="client")
        self.panier = None
    def parcourir_catalogue(self,catalogue):
        pass
    def filter_products(self, *args, category):
        pass

    def ajouter_au_panier(self, produit_id, quantite):
        pass

    def passer_commande(self):
        pass

    def voir_historique_commandes(self):
        pass