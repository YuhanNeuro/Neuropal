import os
import shutil
from datetime import datetime
from openai import OpenAI
from tqdm import tqdm 

def initialiser_client_llm():
    print("Initialisation du client LLM.")
    return OpenAI(base_url="http://localhost:4444/v1", api_key="lm-studio")

def configurer_chemins():
    print("Configuration des chemins des répertoires.")
    dirs = {
        'source_dir': r"C:\Users\x\Desktop\NeuroPal_Global\Programmes\Modules\2_Neuropal_Traitement\0_Architecture_pipeline\04_Output_llm",
        'history_dir': r"C:\Users\x\Desktop\NeuroPal_Global\Programmes\Modules\2_Neuropal_Traitement\0_Architecture_pipeline\05_Output_orga\history_orga",
        'output_dir': r"C:\Users\x\Desktop\NeuroPal_Global\Programmes\Modules\2_Neuropal_Traitement\0_Architecture_pipeline\05_Output_orga",
        'extract_history_dir': r"C:\Users\x\Desktop\NeuroPal_Global\Programmes\Modules\2_Neuropal_Traitement\0_Architecture_pipeline\05_Output_orga\history_orga"
    }

    # Création des répertoires s'ils n'existent pas
    for dir_path in dirs.values():
        os.makedirs(dir_path, exist_ok=True)

    print(f"Répertoires vérifiés ou créés.")
    return dirs


def supprimer_contenu_dossier(dossier):
    for item in os.listdir(dossier):
        item_path = os.path.join(dossier, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    print(f"Le contenu du répertoire {dossier} a été supprimé.")

def filtrer_longueur_lignes(contenu):
    return "\n".join(ligne for ligne in contenu.splitlines() if len(ligne) <= 80)

client = initialiser_client_llm()
dirs = configurer_chemins()

already_processed = set(os.listdir(dirs['history_dir']))
print("Début du traitement des fichiers.")

for filename in os.listdir(dirs['source_dir']):
    if filename not in already_processed and not filename.startswith('history'):
        paths = {
            'source_file': os.path.join(dirs['source_dir'], filename),
            'history_file': os.path.join(dirs['history_dir'], filename),
            'output_file': os.path.join(dirs['output_dir'], f"output_{filename}")
        }

        print(f"Traitement du fichier {filename}.")
        shutil.copy2(paths['source_file'], paths['history_file'])

        with open(paths['source_file'], 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        print("Interaction avec le modèle LLM.")
        history = [{"role": "system", "content": "Divide your answer into two categories: events and tasks. For each item, provide your answer in this format: 'categories - Date - Subject'. Always answer in French."},
                   {"role": "user", "content": content}]
        
        completion = client.chat.completions.create(
            model="NousResearch/Hermes-2-Pro-Mistral-7B-GGUF/Hermes-2-Pro-Mistral-7B.Q4_0.gguf",
            messages=history,
            temperature=0.7,
            stream=True,
        )

        pbar = tqdm(desc="Traitement LLM en cours")
        new_message_content = []

        for chunk in completion:
            if chunk.choices[0].delta.content:
                new_message_content.append(chunk.choices[0].delta.content)
                pbar.update(len(chunk.choices[0].delta.content))
        pbar.close()

        print("Interaction avec le modèle LLM terminée.")
        filtered_output = filtrer_longueur_lignes("".join(new_message_content))
        with open(paths['output_file'], 'w', encoding='utf-8') as outfile:
            outfile.write(filtered_output)
        print(f"La sortie filtrée pour {filename} a été enregistrée dans {paths['output_file']}.")

        supprimer_contenu_dossier(r"C:\tmp")
