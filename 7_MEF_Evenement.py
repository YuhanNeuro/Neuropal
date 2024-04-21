import pandas as pd
import os
from glob import glob

# Chemins nécessaires
chemin_repertoire = r'C:\Users\x\Desktop\NeuroPal_Global\Base_de_donnees\3_Extraction_donnees\2_Extraction_evenement'
chemin_fichier_excel = os.path.join(chemin_repertoire, 'Evenements.xlsx')
chemin_fichier_historique = r'C:\Users\x\Desktop\NeuroPal_Global\Base_de_donnees\2_Historiques\history_Evenement_list\history_Evenement_list.txt'

# Assurez-vous que le dossier d'historique existe
os.makedirs(os.path.dirname(chemin_fichier_historique), exist_ok=True)

# Lire l'historique des fichiers déjà traités
if os.path.exists(chemin_fichier_historique):
    with open(chemin_fichier_historique, 'r', encoding='utf-8') as fichier_historique:
        fichiers_traites = set(fichier_historique.read().splitlines())
else:
    fichiers_traites = set()
    # Créer le fichier d'historique vide s'il n'existe pas
    with open(chemin_fichier_historique, 'w', encoding='utf-8') as fichier_historique:
        pass

# Fonction pour lire et traiter chaque fichier texte
def traiter_fichier_texte(chemin):
    donnees = []
    with open(chemin, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            if ligne.strip():  # Ignorer les lignes vides
                parties = ligne.split(':')
                date = parties[0].split('-')[1].strip()
                description = parties[1].strip()
                donnees.append({'Date': date, 'Description': description})
    return donnees

# Vérifier si le fichier Excel existe déjà
if os.path.exists(chemin_fichier_excel):
    df_existante = pd.read_excel(chemin_fichier_excel)
else:
    df_existante = pd.DataFrame(columns=['Date', 'Description'])

# Lister tous les fichiers texte dans le répertoire spécifié
fichiers_texte = glob(os.path.join(chemin_repertoire, '*.txt'))
fichiers_a_traiter = [f for f in fichiers_texte if f not in fichiers_traites]

# Traiter chaque fichier texte non traité et mettre à jour le DataFrame
for fichier in fichiers_a_traiter:
    nouvelles_donnees = traiter_fichier_texte(fichier)
    df_nouvelles = pd.DataFrame(nouvelles_donnees)
    df_existante = pd.concat([df_existante, df_nouvelles], ignore_index=True)
    fichiers_traites.add(fichier)

# Enregistrer le DataFrame mis à jour dans le fichier Excel
df_existante.to_excel(chemin_fichier_excel, index=False)

# Mettre à jour l'historique des fichiers traités
with open(chemin_fichier_historique, 'w', encoding='utf-8') as fichier_historique:
    fichier_historique.write('\n'.join(fichiers_traites))
