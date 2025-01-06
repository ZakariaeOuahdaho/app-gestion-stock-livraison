from datetime import datetime
from typing import List, Dict

class Produit:
    def __init__(self, id: int, nom: str, description: str, prix: float, quantite: int, categorie: str):
        self.id = id
        self.nom = nom
        self.description = description
        self.prix = prix
        self.quantite = quantite
        self.categorie = categorie

    def __str__(self):
        return f"{self.nom} - {self.prix}€ (Stock: {self.quantite})"

    def reduire_stock(self, quantite: int) -> bool:
        if self.quantite >= quantite:
            self.quantite -= quantite
            return True
        return False

    def augmenter_stock(self, quantite: int):
        self.quantite += quantite

class Utilisateur:
    def __init__(self, id: int, nom: str, mot_de_passe: str, role: str):
        self.id = id
        self.nom = nom
        self.mot_de_passe = mot_de_passe
        self.role = role

class Client(Utilisateur):
    def __init__(self, id: int, nom: str, mot_de_passe: str):
        super().__init__(id, nom, mot_de_passe, "client")
        self.panier = Panier()

    def ajouter_au_panier(self, produit: Produit, quantite: int) -> bool:
        if produit.quantite >= quantite:
            self.panier.ajouter_produit(produit, quantite)
            return True
        return False

    def voir_panier(self):
        return self.panier.voir_contenu()

class Admin(Utilisateur):
    def __init__(self, id: int, nom: str, mot_de_passe: str):
        super().__init__(id, nom, mot_de_passe, "admin")

    def ajouter_produit(self, inventaire, produit: Produit):
        inventaire.ajouter_produit(produit)

    def modifier_produit(self, inventaire, id_produit: int, **modifications):
        inventaire.modifier_produit(id_produit, modifications)

class Panier:
    def __init__(self):
        self.produits: Dict[Produit, int] = {}  # produit: quantité
        self.date_creation = datetime.now()

    def ajouter_produit(self, produit: Produit, quantite: int):
        if produit in self.produits:
            self.produits[produit] += quantite
        else:
            self.produits[produit] = quantite

    def retirer_produit(self, produit: Produit):
        if produit in self.produits:
            del self.produits[produit]

    def modifier_quantite(self, produit: Produit, quantite: int):
        if quantite <= 0:
            self.retirer_produit(produit)
        else:
            self.produits[produit] = quantite

    def calculer_total(self) -> float:
        return sum(produit.prix * quantite for produit, quantite in self.produits.items())

    def voir_contenu(self) -> str:
        if not self.produits:
            return "Panier vide"
        
        contenu = "Contenu du panier:\n"
        for produit, quantite in self.produits.items():
            contenu += f"{produit.nom} x{quantite} = {produit.prix * quantite}€\n"
        contenu += f"\nTotal: {self.calculer_total()}€"
        return contenu

class Inventaire:
    def __init__(self):
        self.produits: List[Produit] = []

    def ajouter_produit(self, produit: Produit):
        self.produits.append(produit)

    def supprimer_produit(self, id_produit: int):
        self.produits = [p for p in self.produits if p.id != id_produit]

    def modifier_produit(self, id_produit: int, modifications: dict):
        for produit in self.produits:
            if produit.id == id_produit:
                for key, value in modifications.items():
                    setattr(produit, key, value)
                break

    def rechercher_produit(self, critere: str, valeur: str) -> List[Produit]:
        return [p for p in self.produits if str(getattr(p, critere)).lower() == str(valeur).lower()]

    def filtrer_par_categorie(self, categorie: str) -> List[Produit]:
        return [p for p in self.produits if p.categorie.lower() == categorie.lower()]

class Commande:
    def __init__(self, client: Client, panier: Panier):
        self.client = client
        self.produits = panier.produits.copy()
        self.total = panier.calculer_total()
        self.date = datetime.now()
        self.statut = "En attente"

    def valider_commande(self):
        self.statut = "Validée"
        # Réduire le stock des produits
        for produit, quantite in self.produits.items():
            produit.reduire_stock(quantite)

    def annuler_commande(self):
        if self.statut == "Validée":
            # Restaurer le stock des produits
            for produit, quantite in self.produits.items():
                produit.augmenter_stock(quantite)
        self.statut = "Annulée"

# Exemple d'utilisation
def main():
    # Création de l'inventaire
    inventaire = Inventaire()

    # Création de quelques produits
    produits = [
        Produit(1, "Pommes", "Pommes verte", 2.5, 100, "Fruits"),
        Produit(2, "Pain", "Pain", 1.0, 50, "Boulangerie"),
        Produit(3, "Lait", "Lait 1 L", 1.5, 30, "Produits laitiers")
    ]

    # Ajout des produits à l'inventaire
    for produit in produits:
        inventaire.ajouter_produit(produit)

    # Création d'un client
    client = Client(1, "saad", "password")

    # Ajout de produits au panier
    client.ajouter_au_panier(produits[0], 5)  # 5 pommes
    client.ajouter_au_panier(produits[1], 2)  # 2 pains

    # Affichage du panier
    print(client.voir_panier())

    # Création d'une commande
    commande = Commande(client, client.panier)
    commande.valider_commande()

    # Vérification du stock après la commande
    print("\nStock après la commande:")
    for produit in inventaire.produits:
        print(f"{produit.nom}: {produit.quantite}")

if __name__ == "__main__":
    main()