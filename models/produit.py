class Produit:
    def __init__(self, id=None, nom="", description="", prix=0, quantite=0, categorie_id=None):
        self.id = id
        self.nom = nom
        self.description = description
        self.prix = prix
        self.quantite = quantite
        self.categorie_id = categorie_id