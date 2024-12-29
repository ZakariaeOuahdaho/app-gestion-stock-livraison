from datetime import datetime
# Classe Notification
class Notification:
    @staticmethod
    def envoyerNotification(client, message):
        # Simule l'envoi d'une notification à un client
        print(f"Notification pour {client.nom} ({client.email}): {message}")

# Classe Client
class Client:
    def __init__(self, idClient, nom, email, adresse, motDePasse):
        self.idClient = idClient
        self.nom = nom
        self.email = email
        self.adresse = adresse
        self.motDePasse = motDePasse
        self.panier = Panier()

    def parcourirCatalogue(self, catalogue):
        return catalogue.listeProduits

    def ajouterAuPanier(self, produit, quantite):
        self.panier.ajouterArticle(produit, quantite)

    def passerCommande(self):
        commande = Commande(self, self.panier.listeArticles)
        Notification.envoyerNotification(self, f"Votre commande avec l'ID {commande.idCommande} a été passée avec succès.")
        return commande

    def suivreCommande(self, commande):
        return commande.etat

# Classe Produit
class Produit:
    def __init__(self, idProduit, nom, description, prix, categorie, quantiteEnStock):
        self.idProduit = idProduit
        self.nom = nom
        self.description = description
        self.prix = prix
        self.categorie = categorie
        self.quantiteEnStock = quantiteEnStock

    def mettreAJourStock(self, nouvelleQuantite):
        self.quantiteEnStock = nouvelleQuantite

    def ajusterPrix(self, nouveauPrix):
        self.prix = nouveauPrix

# Classe Panier
class Panier:
    def __init__(self):
        self.idPanier = None
        self.listeArticles = []
        self.total = 0

    def ajouterArticle(self, produit, quantite):
        if quantite > produit.quantiteEnStock:
            print(f"Erreur: Stock insuffisant pour {produit.nom}")
            return
        self.listeArticles.append({"produit": produit, "quantite": quantite})
        produit.mettreAJourStock(produit.quantiteEnStock - quantite)
        self.calculerTotal()

    def retirerArticle(self, produit):
        self.listeArticles = [article for article in self.listeArticles if article["produit"] != produit]
        self.calculerTotal()

    def calculerTotal(self):
        self.total = sum(article["produit"].prix * article["quantite"] for article in self.listeArticles)
        return self.total

# Classe Commande
class Commande:
    id_counter = 1000  # ID de départ pour la génération dynamique

    def __init__(self, client, listeArticles):
        self.idCommande = Commande.id_counter
        Commande.id_counter += 1
        self.client = client
        self.listeArticles = listeArticles
        self.etat = "commande en préparation"
        self.dateCommande = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.modeLivraison = None

    def mettreAJourEtat(self, nouvelEtat):
        self.etat = nouvelEtat
        Notification.envoyerNotification(self.client, f"Votre commande est maintenant à l'état : {self.etat}")

    def calculerTotal(self):
        return sum(article["produit"].prix * article["quantite"] for article in self.listeArticles)

    def annulerCommande(self):
        self.etat = "Annulée"
        Notification.envoyerNotification(self.client, "Votre commande a été annulée.")

# Classe Livreur
class Livreur:
    def __init__(self, idLivreur, nom, vehicule, zoneDeLivraison):
        self.idLivreur = idLivreur
        self.nom = nom
        self.vehicule = vehicule
        self.zoneDeLivraison = zoneDeLivraison

    def recevoirCommande(self, commande):
        self.commande = commande
        self.etatLivraison = "commande en route"

    def mettreAJourStatutLivraison(self, statut):
        self.etatLivraison = statut
        Notification.envoyerNotification(self.commande.client, f"Statut de votre livraison : {self.etatLivraison}")
        return self.etatLivraison

# Classe Administrateur
class Administrateur:
    def __init__(self, idAdmin, nom, email, motDePasse):
        self.idAdmin = idAdmin
        self.nom = nom
        self.email = email
        self.motDePasse = motDePasse

    def ajouterProduit(self, catalogue, produit):
        catalogue.listeProduits.append(produit)

    def modifierProduit(self, catalogue, idProduit, nouveauProduit):
        for i, produit in enumerate(catalogue.listeProduits):
            if produit.idProduit == idProduit:
                catalogue.listeProduits[i] = nouveauProduit

    def surveillerStock(self, catalogue):
        return {produit.nom: produit.quantiteEnStock for produit in catalogue.listeProduits}

    def analyserPerformances(self, commandes):
        # Retourne le nombre de commandes et total des ventes
        totalVentes = sum(commande.calculerTotal() for commande in commandes)
        return {"nombre des commandes": len(commandes), "Total des Ventes": totalVentes}

# Classe Paiement
class Paiement:
    def __init__(self, idPaiement, montant, datePaiement, methodePaiement):
        self.idPaiement = idPaiement
        self.montant = montant
        self.datePaiement = datePaiement
        self.methodePaiement = methodePaiement

    def effectuerPaiement(self):
        return f"Paiement de {self.montant}DHS effectué avec {self.methodePaiement}"

    def rembourser(self):
        return f"Remboursement de {self.montant}DHS a été effectué"

class Catalogue:
    def __init__(self):
        self.listeProduits = []

    def filtrerParCategorie(self, categorie):
        return [produit for produit in self.listeProduits if produit.categorie == categorie]

    def rechercherProduit(self, nom):
        return [produit for produit in self.listeProduits if nom.lower() in produit.nom.lower()]

# Création des premiers produits de notre Supermarché en ligne
catalogue = Catalogue()
produit1 = Produit(1, "Pommes", "Pommes bio", 11.50, "Fruits", 100)
produit2 = Produit(2, "Tomates", "Tomates fraîches", 10.00, "Légumes", 50)
produit3 = Produit(3, "Savon", "Taouss", 10.00, "Produits cosmétiques", 200)

# Ajout des produits au catalogue
catalogue.listeProduits.extend([produit1, produit2, produit3])

# Création du premier client
client = Client(1, "Zakaria Itahriouan", "z.itahriouan@gmail.com", "15 Rue Exemple Moulay Ismail", "PassWord188")

# Le client parcourt le catalogue
print("Produits disponibles dans le catalogue:")
for produit in client.parcourirCatalogue(catalogue):
    print(f"{produit.nom} - {produit.prix} DHS")

# Le client ajoute des produits à son panier
client.ajouterAuPanier(produit1, 3) 
client.ajouterAuPanier(produit2, 2)

# Affichage du panier
print("\nPanier du client:")
for article in client.panier.listeArticles:
    print(f"{article['produit'].nom} - {article['quantite']} unités")

# Total du panier
total_panier = client.panier.calculerTotal()
print(f"\nTotal du panier: {total_panier} DHS")

# Le client passe la commande
commande = client.passerCommande()
print("\nCommande passée. Etat:", commande.etat)

# Le client suit la commande
etat_commande = client.suivreCommande(commande)
print("Etat de la commande:", etat_commande)

# Création des administrateurs
admin1 = Administrateur(1, "Saad Korchi", "saad.korchi@eidia.ueuromed.org", "adminbasmos1")
admin2 = Administrateur(2, "Zakariae Ouahdaho", "zakariae.ouahdaho@eidia.ueuromed.org", "adminbasmos2")

# Le premier administrateur surveille le stock
stock = admin1.surveillerStock(catalogue)
print("\nQuantité en stock des produits:")
for produit, quantite in stock.items():
    print(f"{produit}: {quantite} en stock")

# Le deuxième administrateur analyse les performances des ventes
performances = admin2.analyserPerformances([commande])
print("\nAnalyse des performances des ventes:")
print(f"Nombre de commandes : {performances['nombre des commandes']}")
print(f"Total des ventes : {performances['Total des Ventes']} DHS")
