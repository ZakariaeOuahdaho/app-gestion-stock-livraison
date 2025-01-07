class Panier:
    def __init__(self, utilisateur_id):
        self.utilisateur_id = utilisateur_id
        self.items = {}
        self.date_creation = None

    def ajouter_produit(self, produit_id, quantite):
        pass

    def retirer_produit(self, produit_id):
        pass

    def modifier_quantite(self, produit_id, quantite):
        pass

    def calculer_total(self):
        pass

    def vider_panier(self):
        pass

    def get_contenu_panier(self):
        pass