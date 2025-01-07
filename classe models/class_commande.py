class Commande:
    def __init__(self, id=None, utilisateur_id=None, total=0, date_commande=None, statut="En attente"):
        self.id = id
        self.utilisateur_id = utilisateur_id
        self.total = total
        self.date_commande = date_commande
        self.statut = statut
        self.produits = []

    def ajouter_produit(self, produit, quantite):
        pass

    def calculer_total(self):
        pass

    def changer_statut(self, nouveau_statut):
        pass

    def annuler(self):
        pass

    def get_details(self):
        pass