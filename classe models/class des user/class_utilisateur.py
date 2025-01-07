class Utilisateur:
    def __init__(self, id=None, nom_utilisateur="", mot_de_passe="", role=""):
        self.id = id
        self.nom_utilisateur = nom_utilisateur
        self.mot_de_passe = mot_de_passe
        self.role = role

    def verifier_mot_de_passe(self, mot_de_passe):
        pass

    def changer_mot_de_passe(self, ancien_mdp, nouveau_mdp):
        pass

    def get_role(self):
        pass