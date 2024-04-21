import pandas as pd
from datetime import datetime

# Chemin du fichier Excel
fichier_excel = r"C:\Users\x\Desktop\NeuroPal_Global\Base_de_donnees\4_Donnees_interface\0_calendar\dates_and_days_with_week_number_2024.xlsx"

# Lire le fichier Excel
df = pd.read_excel(fichier_excel)

# Définir la date d'aujourd'hui
aujourdhui = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Trouver la localisation de la date d'aujourd'hui dans la colonne B
try:
    index_date = df[df['Date'] == aujourdhui].index[0]
except IndexError:
    # Si la date exacte à la seconde près n'est pas trouvée, on peut essayer sans les heures, minutes, secondes
    aujourdhui = datetime.now().strftime("%d/%m/%Y 00:00:00")
    index_date = df[df['Date'] == aujourdhui].index[0]

# Calculer l'index des lignes à récupérer
index_min = max(index_date - 15, 0)  # pour éviter un index négatif
index_max = min(index_date + 15, len(df) - 1)  # pour éviter un index hors des limites

# Extraire les 30 lignes centrées autour de la date d'aujourd'hui
resultat = df.iloc[index_min:index_max + 1]

# Afficher le résultat
print(resultat)

# Chemin pour sauvegarder le résultat
chemin_sauvegarde = r"C:\Users\x\Desktop\NeuroPal_Global\Base_de_donnees\2_Historiques\history_4semaines\4semaine.xlsx"

# Enregistrer le résultat dans un fichier Excel
resultat.to_excel(chemin_sauvegarde, index=False)
