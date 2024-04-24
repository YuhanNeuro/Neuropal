import torch  # Importation de torch pour la gestion des périphériques
from audio import AudioRecorder
from speech import SpeechSynthesizer
from transcription import AudioTranscriber
from llm_communication import LLMClient  # Importation du module de communication LLM
from audio_visualizer import AudioVisualizer  # Importation du module de visualisation audio
import threading  # Importation du module threading pour gérer les threads

def main():
    # Initialisation des composants
    recorder = AudioRecorder()
    synthesizer = SpeechSynthesizer()
    device = "cuda" if torch.cuda.is_available() else "cpu"  # Utilisation explicite de torch ici
    transcriber = AudioTranscriber(model_type="medium", device=device)
    llm_client = LLMClient(base_url="http://localhost:4444/v1", api_key="lm-studio")  # Instance du client LLM
    visualizer = AudioVisualizer()  # Instance du visualisateur audio

    # Définir une fonction pour démarrer la visualisation dans un thread
    def start_visualization():
        while True:
            visualizer.start_visualization()  # Démarre la visualisation audio

    # Création et démarrage du thread de visualisation
    visualization_thread = threading.Thread(target=start_visualization)
    visualization_thread.daemon = True  # Ce thread est un processus de fond qui s'arrête avec le programme
    visualization_thread.start()

    # Interaction principale
    try:
        while True:
            synthesizer.speak("Je vous écoute.")
            audio_data = recorder.record_audio()
            file_path = recorder.save_audio(audio_data)
            text = transcriber.audio_to_text(file_path)
            print(f"Transcription : {text}")  # Affichage de la transcription

            # Vérifier si la transcription est vide ou ne contient qu'un mot
            if not text.strip() or len(text.split()) <= 3:
                print("Le texte transcrit est vide ou insuffisant pour une réponse.")
                continue  # Ignore l'interaction avec le LLM si la transcription est vide ou trop courte

            # Obtention de la réponse du modèle LLM
            response_llm = llm_client.get_response(text)
            print("Pour vous répondre :", response_llm)  # Affichage de la réponse du LLM
            synthesizer.speak(response_llm)  # La synthèse vocale de la réponse du LLM

    except KeyboardInterrupt:
        print("Arrêt du programme.")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")

if __name__ == "__main__":
    main()
