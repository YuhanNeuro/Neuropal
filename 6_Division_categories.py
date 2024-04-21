import os
import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta

# Chemins d'accès aux dossiers
input_path = "C:\\Users\\x\\Desktop\\NeuroPal_Global\\Programmes\\Modules\\2_Neuropal_Traitement\\0_Architecture_pipeline\\05_Output_orga"
history_path = "C:\\Users\\x\\Desktop\\NeuroPal_Global\\Base_de_donnees\\2_Historiques\\history_categories"
output_task_path = "C:\\Users\\x\\Desktop\\NeuroPal_Global\\Base_de_donnees\\3_Extraction_donnees\\1_Extraction_task"
output_event_path = "C:\\Users\\x\\Desktop\\NeuroPal_Global\\Base_de_donnees\\3_Extraction_donnees\\2_Extraction_evenement"

# Fonction pour normaliser les dates
def normalize_date(date_str):
    if "Demain" in date_str:
        return datetime.datetime.today() + relativedelta(days=+1)
    try:
        return parser.parse(date_str, dayfirst=True, default=datetime.datetime.today())
    except:
        return None

# Chargement de l'historique
def load_history():
    try:
        with open(os.path.join(history_path, "history.txt"), "r", encoding='utf-8') as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

# Mise à jour de l'historique
def update_history(history, filename):
    with open(os.path.join(history_path, "history.txt"), "a", encoding='utf-8') as file:
        file.write(filename + '\n')
    history.add(filename)

# Lire les fichiers du dossier input et traiter les données
def process_files():
    history = load_history()
    tasks = []
    events = []
    
    for filename in os.listdir(input_path):
        if filename.endswith(".txt") and filename not in history:
            with open(os.path.join(input_path, filename), "r", encoding='utf-8') as file:
                data = file.readlines()
            
            for item in data:
                parts = item.strip().split(" : ")
                if len(parts) < 2:
                    continue
                type_date = parts[0].split(" - ")
                item_type = type_date[0].split(". ")[1].strip()
                original_line = item.strip()
                
                if "Tâche" in item_type:
                    tasks.append(original_line)
                elif "Événement" in item_type:
                    events.append(original_line)

            update_history(history, filename)

    # Écriture des résultats dans des fichiers
    today = datetime.datetime.today().strftime('%Y%m%d')
    with open(os.path.join(output_task_path, f"{today}_Tâche.txt"), 'w', encoding='utf-8') as file:
        for task in tasks:
            file.write(task + '\n')

    with open(os.path.join(output_event_path, f"{today}_Événement.txt"), 'w', encoding='utf-8') as file:
        for event in events:
            file.write(event + '\n')

# Exécuter le traitement des fichiers
process_files()
