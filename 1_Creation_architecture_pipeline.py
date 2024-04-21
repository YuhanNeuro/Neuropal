import os

# Chemin de base où les dossiers principaux seront créés
base_path = r"C:\Users\x\Desktop\NeuroPal_Global\Programmes\Modules\2_Neuropal_Traitement\0_Architecture_pipeline"

# Dictionnaire définissant la structure des dossiers et sous-dossiers
folder_structure = {
    "01_Extrac_phone": ["history_segment"],
    "02_Audiofiles": ["history_audio"],
    "03_Transcription": ["history_transcription"],
    "04_Output_llm": ["history_llm"],
    "05_Output_llm_infos": ["history_llm_infos"],
    "06_Suggestion_llm": ["history_suggestion"],
}

# Boucle pour créer chaque dossier et sous-dossier
for main_folder, sub_folders in folder_structure.items():
    # Construire le chemin du dossier principal
    main_folder_path = os.path.join(base_path, main_folder)
    # Créer le dossier principal s'il n'existe pas
    if not os.path.exists(main_folder_path):
        os.makedirs(main_folder_path)
        print(f"Dossier principal créé : {main_folder_path}")
    else:
        print(f"Le dossier principal existe déjà : {main_folder_path}")
    
    # Créer les sous-dossiers
    for sub_folder in sub_folders:
        # Construire le chemin du sous-dossier
        sub_folder_path = os.path.join(main_folder_path, sub_folder)
        # Créer le sous-dossier s'il n'existe pas
        if not os.path.exists(sub_folder_path):
            os.makedirs(sub_folder_path)
            print(f"Sous-dossier créé : {sub_folder_path}")
        else:
            print(f"Le sous-dossier existe déjà : {sub_folder_path}")
