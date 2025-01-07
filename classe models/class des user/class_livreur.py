class Livreur(Utilisateur):
    def __init__(self, id=None, nom_utilisateur="", mot_de_passe=""):
        super().__init__(id, nom_utilisateur, mot_de_passe, role="livreur")
        self.livraisons = []

    def voir_livraisons_disponibles(self):
        pass

    def accepter_livraison(self, livraison_id):
        pass

    def completer_livraison(self, livraison_id):
        pass

    def voir_historique_livraisons(self):
        pass