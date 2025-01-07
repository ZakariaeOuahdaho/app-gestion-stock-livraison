class Admin(Utilisateur):
    def __init__(self, id=None, nom_utilisateur="", mot_de_passe=""):
        super().__init__(id, nom_utilisateur, mot_de_passe, role="admin")

    def ajouter_produit(self, produit):
        pass

    def modifier_produit(self, produit_id, modifications):
        pass

    def supprimer_produit(self, produit_id):
        pass

    def voir_statistiques(self):
        pass

    def gerer_utilisateurs(self):
        pass