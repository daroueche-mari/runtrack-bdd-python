import mysql.connector

# Connexion directe
db = mysql.connector.connect(
    host="10.10.10.117",
    user="student",
    password="MotDePasseSolide",
    database="qui_est_ce",
)

cursor = db.cursor()

# cursor.execute("SELECT * FROM attributs")
# cursor.execute("SELECT p.nom AS personnage, GROUP_CONCAT(a.nom ORDER BY a.nom) AS attributs FROM personnages p JOIN personnage_attribut pa ON p.id = pa.id_personnage JOIN attributs a ON pa.id_attribut = a.id GROUP BY p.id ORDER BY RAND() LIMIT 1;")
cursor.execute("SELECT * FROM personnage_attribut WHERE id_attribut = 16")

resultats = cursor.fetchall()
print(resultats)

cursor.close()
db.close()

# barbe non, moustache non, tatouage oui, yeux bleu oui









# [('Oscar', 'cheveux_noirs,echarpe,yeux_bleus,yeux_marron,yeux_noirs')]
