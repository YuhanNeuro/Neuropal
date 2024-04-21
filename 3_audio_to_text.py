import os
import whisper
from datetime import datetime

# Définition des chemins
audio_folder = "C:\\Users\\x\\Desktop\\NeuroPal_Global\\Programmes\\Modules\\2_Neuropal_Traitement\\0_Architecture_pipeline\\02_Audiofiles"
transcription_folder = "C:\\Users\\x\\Desktop\\NeuroPal_Global\\Programmes\\Modules\\2_Neuropal_Traitement\\0_Architecture_pipeline\\03_Transcription"
history_folder = "C:\\Users\\x\\Desktop\\NeuroPal_Global\\Programmes\\Modules\\2_Neuropal_Traitement\\0_Architecture_pipeline\\03_Transcription\\history_transcription"

# Chargement du modèle Whisper
model = whisper.load_model("medium")

# Vérification et création des dossiers si nécessaire
os.makedirs(transcription_folder, exist_ok=True)
os.makedirs(history_folder, exist_ok=True)

# Transcription de chaque fichier audio
for filename in os.listdir(audio_folder):
    if filename.endswith(".mp3") or filename.endswith(".wav"):
        audio_path = os.path.join(audio_folder, filename)
        history_path = os.path.join(history_folder, f"{filename}.txt")

        # Vérification si le fichier a déjà été traité
        if os.path.exists(history_path):
            continue

        # Transcription de l'audio
        result = model.transcribe(audio_path, verbose=False)

        # Enregistrement de la transcription
        transcription_path = os.path.join(transcription_folder, f"{filename}.txt")
        with open(transcription_path, "w", encoding="utf-8") as f:
            f.write(result["text"])

        # Enregistrement des métadonnées
        with open(history_path, "w", encoding="utf-8") as f:
            metadata = {
                "filename": filename,
                "transcription_path": transcription_path,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "language": result["language"]
            }
            for key, value in metadata.items():
                f.write(f"{key}: {value}\n")

print("Transcription terminée.")
