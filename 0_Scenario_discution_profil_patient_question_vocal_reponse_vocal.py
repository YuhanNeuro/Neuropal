import pyttsx3
import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import os
import tempfile
import datetime

# Initialisation du moteur TTS
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Charger le modèle Whisper
model = whisper.load_model("medium")

def speak(text):
    """
    Fonction pour lire à haute voix le texte passé en paramètre.
    """
    engine.say(text)
    engine.runAndWait()

def record_audio(duration=10):
    """
    Enregistre l'audio du microphone pendant une durée spécifiée et retourne le chemin du fichier audio.
    """
    fs = 44100  # Fréquence d'échantillonnage
    print("\nVeuillez parler maintenant...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  # Attendre la fin de l'enregistrement
    temp_file = tempfile.mktemp(suffix=".wav")
    write(temp_file, fs, recording)  # Sauvegarde l'audio temporairement
    return temp_file

def audio_to_text(audio_path):
    """
    Convertit l'audio en texte en utilisant le modèle Whisper.
    """
    result = model.transcribe(audio_path)
    os.remove(audio_path)  # Supprime le fichier audio temporaire
    return result['text']

def pose_question(question, duration=10):
    """
    Pose une question à l'utilisateur, la lit à haute voix, enregistre la réponse vocale et la convertit en texte.
    """
    speak(question)
    audio_path = record_audio(duration)
    reponse = audio_to_text(audio_path)
    print(f"Votre réponse : {reponse}")
    return reponse

# Introduction et collecte du nom
nom_patient = pose_question("Bonjour, je suis Neuropal. Je suis ici aujourd'hui pour mieux vous connaître. "
                            "Puis-je avoir votre nom complet, s'il vous plaît ?")


mots = nom_patient.split()
if len(mots) >= 2:
    deux_derniers_mots = mots[-1:]  # Obtention des deux derniers mots
else:
    deux_derniers_mots = mots  # Si moins de deux mots, prendre ce qui est disponible

# Conversion des deux derniers mots en une chaîne pour l'utilisation dans la salutation
nom_pour_salutation = ' '.join(deux_derniers_mots)

# Salutation du patient avec les deux derniers mots de son nom
speak(f"Bonjour Monsieur {nom_pour_salutation}")


# Collecte d'informations générales
informations_generales = {
    "age": pose_question("Quel est votre âge ?"),
    "residence": pose_question("Où habitez-vous actuellement ?"),
    "contacts_urgence": pose_question("Avez-vous des contacts d'urgence ? Si oui, pourriez-vous me les nommer et me décrire votre relation avec eux ?"),
    "peripeties_medicales": pose_question("Pourriez-vous me parler un peu de vos péripéties médicales ?")
}

# Collecte d'informations sur les traitements médicamenteux
traitements_medicaux = {
    "prend_traitements": pose_question("Prenez-vous des traitements médicamenteux en ce moment ?")
}

# Vérifie si le patient prend des traitements avant de poser la question sur les détails
if "oui" in traitements_medicaux["prend_traitements"].lower():
    traitements_medicaux["details_traitements"] = pose_question("Pourriez-vous me dire lesquels et pourquoi vous les prenez ?")
else:
    traitements_medicaux["details_traitements"] = "Corps à toute épreuve"

# Collecte d'informations sur les allergies ou intolérances
allergies_intolerances = {
    "a_allergies": pose_question("Avez-vous des allergies ou des intolérances que nous devrions connaître ?")
}

# Vérifie si le patient a des allergies avant de poser la question sur les détails
if "oui" in allergies_intolerances["a_allergies"].lower():
    allergies_intolerances["details_allergies"] = pose_question("Si oui, pourriez-vous m'expliquer votre cas spécifique ?")
else:
    allergies_intolerances["details_allergies"] = "Corps à toute épreuve"

# Collecte d'autres informations via des questions supplémentaires
questions_supplementaires = {
    "passe_temps": pose_question("Quels sont vos passe-temps et intérêts ?"),
    "preferences_alimentaires": pose_question("Avez-vous des préférences alimentaires ou des restrictions ?"),
    "animaux_de_compagnie": pose_question("Avez-vous des animaux de compagnie ? Si oui, pourriez-vous me parler d'eux ?")
}

# Résumé des informations collectées à la fin de l'entretien
print("Merci pour vos réponses.")



# Création d'un résumé des réponses
resume = f"""
Nom du patient: {nom_patient}
Informations générales: {informations_generales}
Traitements médicaux: {traitements_medicaux}
Allergies et intolérances: {allergies_intolerances}
Questions supplémentaires: {questions_supplementaires}
"""

print("Merci pour vos réponses. Voici un résumé de notre entretien :")
print(resume)

# Générer le nom du fichier avec la date du jour et l'identifiant du patient
date_du_jour = datetime.datetime.now().strftime("%Y-%m-%d")
identifiant_patient = nom_patient.replace(" ", "_")
nom_fichier = f"{date_du_jour}_{identifiant_patient}.txt"

# Chemin du fichier où le script est exécuté
chemin_fichier = "C:\\Users\\x\\Desktop\\NeuroPal_Global\\Base_de_donnees\\1_Profil_Patient"

# Écrire le résumé dans un fichier texte
with open(chemin_fichier, "w", encoding="utf-8") as fichier:
    fichier.write(resume)

print(f"Le résumé a été enregistré dans le fichier {nom_fichier}")

