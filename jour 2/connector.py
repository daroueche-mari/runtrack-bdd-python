import mysql.connector

# Connexion directe
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root", 
    database="LaPlateforme"
)

cursor = db.cursor()

# 1. Vérifie bien si ta table s'appelle 'etudiant' ou 'etudiants' (souvent au pluriel)
cursor.execute("SELECT * FROM salle")

# 2. Utilise un nom au pluriel pour la liste (ex: tous_les_etudiants)
resultats = cursor.fetchall()

# 3. On boucle sur les résultats
for etudiant in resultats:
    print(etudiant)

# Fermeture propre
cursor.close()
db.close()