class Livraison:
    def __init__(self, id=None, commande_id=None, livreur_id=None, adresse="", statut="En attente"):
        self.id = id
        self.commande_id = commande_id
        self.livreur_id = livreur_id
        self.adresse = adresse
        self.statut = statut
        self.date_creation = None
        self.date_livraison = None

    def assigner_livreur(self, livreur_id):
        pass

    def mettre_a_jour_statut(self, nouveau_statut):
        pass

    def completer_livraison(self):
        pass

    def get_details(self):
        pass