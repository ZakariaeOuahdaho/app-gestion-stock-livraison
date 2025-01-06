from database.db import create_connection, close_connection
from mysql.connector import Error

class Panier:
    def __init__(self, utilisateur_id):
        self.utilisateur_id = 2
        self.items = {}  # {produit_id: quantité}
        self.load_panier()

    def load_panier(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT produit_id, quantite 
                    FROM panier 
                    WHERE utilisateur_id = %s
                """, (self.utilisateur_id,))
                for produit_id, quantite in cursor.fetchall():
                    self.items[produit_id] = quantite
            finally:
                cursor.close()
                close_connection(connection)

    def ajouter_produit(self, produit_id, quantite=1):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Vérifier si le produit existe déjà dans le panier
                cursor.execute("""
                    SELECT quantite FROM panier 
                    WHERE utilisateur_id = %s AND produit_id = %s
                """, (self.utilisateur_id, produit_id))
                
                result = cursor.fetchone()
                
                if result:
                    # Mettre à jour la quantité
                    nouvelle_quantite = result[0] + quantite
                    cursor.execute("""
                        UPDATE panier 
                        SET quantite = %s 
                        WHERE utilisateur_id = %s AND produit_id = %s
                    """, (nouvelle_quantite, self.utilisateur_id, produit_id))
                else:
                    # Ajouter nouveau produit
                    cursor.execute("""
                        INSERT INTO panier (utilisateur_id, produit_id, quantite)
                        VALUES (%s, %s, %s)
                    """, (self.utilisateur_id, produit_id, quantite))
                
                connection.commit()
                self.load_panier()
                return True
            except Error as e:
                print(f"Erreur lors de l'ajout au panier: {e}")
                return False
            finally:
                cursor.close()
                close_connection(connection)

    def supprimer_produit(self, produit_id):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM panier 
                    WHERE utilisateur_id = %s AND produit_id = %s
                """, (self.utilisateur_id, produit_id))
                connection.commit()
                self.load_panier()
                return True
            finally:
                cursor.close()
                close_connection(connection)

    def modifier_quantite(self, produit_id, quantite):
        if quantite <= 0:
            return self.supprimer_produit(produit_id)
        
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE panier 
                    SET quantite = %s 
                    WHERE utilisateur_id = %s AND produit_id = %s
                """, (quantite, self.utilisateur_id, produit_id))
                connection.commit()
                self.load_panier()
                return True
            finally:
                cursor.close()
                close_connection(connection)

    def get_contenu_panier(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("""
                    SELECT p.id, p.nom, p.prix, pa.quantite, (p.prix * pa.quantite) as total
                    FROM panier pa
                    JOIN produits p ON pa.produit_id = p.id
                    WHERE pa.utilisateur_id = %s
                """, (self.utilisateur_id,))
                return cursor.fetchall()
            finally:
                cursor.close()
                close_connection(connection)
        return []

    def get_total(self):
        contenu = self.get_contenu_panier()
        return sum(item['total'] for item in contenu)

    def vider_panier(self):
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    DELETE FROM panier 
                    WHERE utilisateur_id = %s
                """, (self.utilisateur_id,))
                connection.commit()
                self.items = {}
                return True
            finally:
                cursor.close()
                close_connection(connection)