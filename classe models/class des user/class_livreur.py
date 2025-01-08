from class_utilisateur import Utilisateur
class Livreur(Utilisateur):
    def __init__(self, id=None, nom_utilisateur="", mot_de_passe=""):
        super().__init__(id, nom_utilisateur, mot_de_passe, role="livreur")
        self.livraisons = []

    def create_delivery_list(self):
        pass
    #avec la base donée 
    def load_deliveries(self):
        pass
    
    def update_statistics(self):
        pass
    
    def filter_deliveries(self):
        pass

    def take_delivery(self):
        pass
    
    def complete_delivery(self):
        pass
    
    def show_delivery_details(self):
        pass
    
    def logout(self):
        pass