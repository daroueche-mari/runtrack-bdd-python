import mysql.connector

class Zoo:
    def __init__(self):
        self.db = mysql.connector.connect(host="localhost", user="root", password="root", database="zoo")
        self.cursor = self.db.cursor()

    # AJOUTER (Animal ou Cage)
    def add_animal(self, nom, race, id_cage, naissance, pays):
        sql = "INSERT INTO animal (nom, race, id_cage, naissance, pays_origine) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (nom, race, id_cage, naissance, pays))
        self.db.commit()

    def add_cage(self, superficie, capacite):
        sql = "INSERT INTO cage (superficie, capacite_max) VALUES (%s, %s)"
        self.cursor.execute(sql, (superficie, capacite))
        self.db.commit()

    # AFFICHER
    def show_all(self):
        print("\n--- Animaux et leurs Cages ---")
        query = "SELECT animal.nom, animal.race, cage.id FROM animal LEFT JOIN cage ON animal.id_cage = cage.id"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            print(f"Animal: {row[0]} ({row[1]}) -> Cage n°{row[2]}")

    # CALCULER SUPERFICIE
    def total_surface(self):
        self.cursor.execute("SELECT SUM(superficie) FROM cage")
        result = self.cursor.fetchone()
        print(f"\n📏 Surface totale : {result[0]} m2")

# --- TEST DIRECT ---
mon_zoo = Zoo()

# On ajoute une cage et un animal pour tester
mon_zoo.add_cage(50.5, 2)
mon_zoo.add_animal("Leo", "Lion", 1, "2020-01-10", "Kenya")

# On affiche les résultats demandés
mon_zoo.show_all()
mon_zoo.total_surface()