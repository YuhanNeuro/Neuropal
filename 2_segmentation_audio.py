from pydub import AudioSegment
from datetime import datetime
import os

# Chemins des dossiers
source_directory = "C:\\Users\\x\\Desktop\\NeuroPal_Global\\Programmes\\Modules\\2_Neuropal_Traitement\\0_Architecture_pipeline\\01_Extrac_phone"
history_directory = "C:\\Users\\x\\Desktop\\NeuroPal_Global\\Programmes\\Modules\\2_Neuropal_Traitement\\0_Architecture_pipeline\\01_Extrac_phone\\history_segment"
output_directory = "C:\\Users\\x\\Desktop\\NeuroPal_Global\\Programmes\Modules\\2_Neuropal_Traitement\\0_Architecture_pipeline\\02_Audiofiles"

# Vérifier et créer le dossier de sortie et l'historique s'ils n'existent pas
for directory in [history_directory, output_directory]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Fichier d'historique
history_file_path = os.path.join(history_directory, "history_log.txt")

# Date actuelle pour nommer les fichiers
current_date = datetime.now().strftime("%Y-%m-%d")

# Parcourir tous les fichiers WAV dans le répertoire source
for filename in os.listdir(source_directory):
    if filename.endswith(".wav"):
        file_path = os.path.join(source_directory, filename)
        
        # Charger le fichier audio
        audio = AudioSegment.from_wav(file_path)

        # Durée du segment en millisecondes (5 minutes * 60 secondes * 1000 millisecondes)
        segment_duration = 5 * 60 * 1000

        for i, start_time in enumerate(range(0, len(audio), segment_duration), 1):
            # Calculer la fin du segment
            end_time = start_time + segment_duration

            # Extraire le segment
            segment = audio[start_time:end_time]

            # Construire le nom du fichier de sortie
            segment_file_name = f"{current_date}_segment_{i}.wav"
            segment_file_path = os.path.join(output_directory, segment_file_name)

            # Exporter le segment
            segment.export(segment_file_path, format="wav")

            # Écrire dans l'historique
            with open(history_file_path, "a") as history_file:
                history_file.write(f"{datetime.now()}: Segment {i} du fichier {filename} exporté en {segment_file_path}\n")

            print(f"Segment {i} exporté: {segment_file_path}")
