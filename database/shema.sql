CREATE TABLE IF NOT EXISTS utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_utilisateur VARCHAR(50) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(50) NOT NULL,
    role ENUM('admin', 'client', 'livreur') NOT NULL
);

-- Insère quelques utilisateurs de test
INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe, role) VALUES 
('admin', 'password', 'admin'),
('saad', '1234', 'client'),
('zakariae', 'password', 'livreur');

CREATE TABLE  categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    description TEXT,
    prix DECIMAL NOT NULL,
    quantite INT NOT NULL,
    categorie_id INT,
    date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categorie_id) REFERENCES categories(id)
);


INSERT INTO categories (nom) VALUES 
('Alimentaire'),
('Boissons'),
('Hygiène'),
('Ménage'),
('Fruits et Légumes');

-- Table des commandes
CREATE TABLE IF NOT EXISTS commandes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    date_commande TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    statut ENUM('En attente', 'Validée', 'En livraison', 'Livrée', 'Annulée') NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
);

-- Table des produits dans les commandes
CREATE TABLE IF NOT EXISTS commande_produits (
    commande_id INT NOT NULL,
    produit_id INT NOT NULL,
    quantite INT NOT NULL,
    prix_unitaire DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (commande_id) REFERENCES commandes(id),
    FOREIGN KEY (produit_id) REFERENCES produits(id),
    PRIMARY KEY (commande_id, produit_id)
);

-- Table des livraisons
CREATE TABLE IF NOT EXISTS livraisons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commande_id INT NOT NULL,
    livreur_id INT,
    adresse_livraison TEXT NOT NULL,
    statut ENUM('En attente', 'En cours', 'Livrée', 'Annulée') NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_livraison TIMESTAMP NULL,
    FOREIGN KEY (commande_id) REFERENCES commandes(id),
    FOREIGN KEY (livreur_id) REFERENCES utilisateurs(id)
);
