import mysql.connector


class ZooManager:
    def __init__(self):
        # Initialisation de la connexion à la base de données
        self.db = mysql.connector.connect(
            host="localhost", user="root", password="root", database="Zoo"
        )
        self.cursor = self.db.cursor()

    # CREATE : Ajouter un animal
    def add_animal(self, nom, race, id_type, naissance, pays_origine):
        # 1. On liste les 5 colonnes
        # 2. On met exactement 5 marqueurs %s
        query = "INSERT INTO animal (nom, race, id_type, naissance, pays_origine) VALUES (%s, %s, %s, %s, %s)"

        # 3. On crée le tuple avec les 5 variables correspondantes (SANS l'id)
        values = (nom, race, id_type, naissance, pays_origine)

        # 4. On exécute en passant la requête ET les valeurs
        self.cursor.execute(query, values)
        self.db.commit()
        print(f"✅ Animal {nom} ajouté !")

    def modify_animal(self, nom, race, id_type, naissance, pays_origine):
        querymodify = "UPDATE animal SET nom = "", race = "", id_type = int,      "

    









    # READ : Récupère et affiche tous les animaux de la table 'animal' et 'cage'
    def show_animal(self):
        # On prépare et on envoie la requête de sélection
        self.cursor.execute("SELECT * FROM animal")

        # On récupère toutes les lignes de la table dans une liste
        resultsanimal = self.cursor.fetchall()

        # On parcourt chaque ligne pour l'afficher dans la console
        for rowanimal in resultsanimal:
            print(rowanimal)

    # READ : Récupère et affiche toutes les cages de la table 'cage'
    def show_cage(self):
        # Exécution de la requête pour lire le contenu de la table 'cage'
        self.cursor.execute("SELECT * FROM cage")

        # Stockage des résultats dans une variable
        resultscage = self.cursor.fetchall()

        # Boucle pour afficher chaque cage (id, numéro, capacité, etc.)
        for rowcage in resultscage:
            print(rowcage)
