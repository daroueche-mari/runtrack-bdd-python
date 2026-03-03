import mysql.connector


class ZooManager:
    def __init__(self):
        # Initialisation de la connexion à la base de données
        self.db = mysql.connector.connect(
            host="localhost", user="root", password="root", database="Zoo"
        )
        self.cursor = self.db.cursor()

    # CREATE : Ajouter un animal et une cage

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

    def add_cage(self, superficie, capacite):
        querycage = "INSERT INTO cage (superficie, capacite) VALUES (%s, %s)"
        valuescage = (superficie, capacite)
        self.cursor.execute(querycage, valuescage)
        self.db.commit()
        print(f"✅ Cage ajouté !")

    # READ : Récupère et affiche tous les animaux de la table 'animal' et 'cage'

    def show_animal(self):
        # On prépare et on envoie la requête de sélection
        self.cursor.execute("SELECT * FROM animal")
        # On récupère toutes les lignes de la table dans une liste
        resultsanimal = self.cursor.fetchall()
        # On parcourt chaque ligne pour l'afficher dans la console
        for rowanimal in resultsanimal:
            print(rowanimal)

    def show_cage(self):
        # Exécution de la requête pour lire le contenu de la table 'cage'
        self.cursor.execute("SELECT * FROM cage")
        # Stockage des résultats dans une variable
        resultscage = self.cursor.fetchall()
        # Boucle pour afficher chaque cage (id, numéro, capacité, etc.)
        for rowcage in resultscage:
            print(rowcage)

    def treatment_size(self):
        sumsql = "SELECT SUM(superficie) FROM cage"
        self.cursor.execute(sumsql)
        self.db.commit()
        print(f"La superficie de toutes les cages est de {sumsql}")

    # UPDATE : Modifier un animal ou une cage via son ID

    def modify_animal(self, animal_id, nom, race, id_type, naissance, pays_origine):
        # 1. On prépare la requête avec des %s pour chaque champ
        # 2. On ajoute WHERE id = %s pour ne cibler qu'UN seul animal
        querymodanimal = """
            UPDATE animal 
            SET nom = %s, race = %s, id_type = %s, naissance = %s, pays_origine = %s 
            WHERE id = %s
        """
        # Les valeurs doivent être dans le même ordre que les %s ci-dessus
        valuesmodanimal = (nom, race, id_type, naissance, pays_origine, animal_id)

        self.cursor.execute(querymodanimal, valuesmodanimal)
        self.db.commit()
        print(f"✅ Animal ID {animal_id} ({nom}) modifié avec succès !")

    def modify_cage(self, cage_id, superficie, capacite):
        # 1. On prépare la requête avec des %s pour chaque champ et On ajoute WHERE id = %s pour ne cibler qu'UN seul animal
        querymodcage = (
            """UPDATE animal SET superficie = %s, capacite = %s, WHERE id = %s"""
        )
        valuesmodcage = (
            superficie,
            capacite,
            cage_id,
        )  # Les valeurs doivent être dans le même ordre que les %s ci-dessus
        self.cursor.execute(querymodcage, valuesmodcage)
        self.db.commit()
        print(f"✅ Cage ID {cage_id} modifié avec succès !")

    # DELETE supprimer un animal

    def delete_animal(self, id_animal):
        # La requête SQL
        sqlanimal = "DELETE FROM animal WHERE id = %s"

        # Exécution avec l'ID passé en paramètre
        self.cursor.execute(sqlanimal, (id_animal,))

        # IMPORTANT : Toujours commit pour valider la suppression en base
        self.db.commit()

        print(f"❌ L'animal avec l'ID {id_animal} a été supprimé.")

    def delete_cage(self, id_cage):
        # La requête SQL
        sqlcage = "DELETE FROM cage WHERE id = %s"

        # Exécution avec l'ID passé en paramètre
        self.cursor.execute(sqlcage, (id_cage,))

        # IMPORTANT : Toujours commit pour valider la suppression en base
        self.db.commit()

        print(f"❌ La Cage ID {id_cage} a été supprimé.")

manager = ZooManager()
manager.add_animal("Lion", "Félin", 39, "2015/01/1", "France")
manager.add_cage(5, 9)