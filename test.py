import customtkinter as ctk

# Configuration de CustomTkinter
ctk.set_appearance_mode("System")  # Modes: "System" (par défaut), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Thèmes: "blue", "green", "dark-blue"

# Création de la fenêtre principale
fenetre = ctk.CTk()
fenetre.title("Supermarché - Gestion des commandes")
fenetre.geometry("500x400")

# Ajout de widgets
label = ctk.CTkLabel(fenetre, text="Bienvenue, Admin", font=("Arial", 20))
label.pack(pady=20)

entry_nom = ctk.CTkEntry(fenetre, placeholder_text="Nom du produit")
entry_nom.pack(pady=10)

entry_prix = ctk.CTkEntry(fenetre, placeholder_text="Prix du produit")
entry_prix.pack(pady=10)

def ajouter_produit():
    nom = entry_nom.get()
    prix = entry_prix.get()
    if nom and prix:
        print(f"Produit ajouté : {nom}, {prix}€")  # Exemple : Ajout à la base de données
    else:
        print("Veuillez remplir tous les champs.")

button = ctk.CTkButton(fenetre, text="Ajouter le produit", command=ajouter_produit)
button.pack(pady=20)

# Lancer l'application
fenetre.mainloop()
