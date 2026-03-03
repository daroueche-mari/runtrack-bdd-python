import mysql.connector

class Employe:
    def __init__(self):
        # Initialisation de la connexion à la base de données
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="entreprise"
        )
        self.cursor = self.db.cursor()

    # CREATE : Ajouter un nouvel employé
    def add(self, last_name, first_name, salary, service_id):
        query = "INSERT INTO employe (nom, prenom, salaire, id_service) VALUES (%s, %s, %s, %s)"
        values = (last_name, first_name, salary, service_id)
        self.cursor.execute(query, values)
        self.db.commit()
        print(f"✅ Employé {first_name} ajouté !")

    # READ : Afficher tous les employés
    def display_all(self):
        self.cursor.execute("SELECT * FROM employe")
        results = self.cursor.fetchall()
        for row in results:
            print(row)

    # UPDATE : Modifier le salaire d'un employé via son ID
    def update_salary(self, emp_id, new_salary):
        query = "UPDATE employe SET salaire = %s WHERE id = %s"
        self.cursor.execute(query, (new_salary, emp_id))
        self.db.commit()
        print(f"🔄 Salaire de l'ID {emp_id} mis à jour !")

    # DELETE : Supprimer un employé via son ID
    def delete(self, emp_id):
        query = "DELETE FROM employe WHERE id = %s"
        self.cursor.execute(query, (emp_id,))
        self.db.commit()
        print(f"❌ Employé ID {emp_id} supprimé !")

# --- ZONE DE TEST ---
if __name__ == "__main__":
    manager = Employe() # Création de l'instance
    
    # Ajout d'un employé de test
    manager.add("Dupont", "Jean", 2500, 25) 
    
    # Mise à jour du salaire pour l'ID 1
    manager.update_salary(1, 3000) 
    
    # Affichage de la table complète
    print("\nContenu de la table :")
    manager.display_all()