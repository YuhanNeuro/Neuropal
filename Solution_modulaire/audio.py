import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import queue
import time

class AudioRecorder:
    def __init__(self, rate=44100, channels=1, threshold=0.05):
        self.rate = rate
        self.channels = channels
        self.threshold = threshold
        self.audio_queue = queue.Queue()
        self.start_time = None  # Pour suivre le début de l'enregistrement

    def callback(self, indata, frames, time, status):
        """Cette fonction de rappel est appelée pour chaque bloc audio."""
        if status:
            print(status)
        # Ajouter le bloc audio à la queue
        self.audio_queue.put(indata.copy())

    def record_audio(self):
        """Enregistre l'audio jusqu'à ce que le silence soit détecté après une phrase."""
        print("Enregistrement en cours...")
        self.start_time = time.time()  # Démarre le chronomètre
        with sd.InputStream(callback=self.callback, channels=self.channels, samplerate=self.rate):
            audio_data = []
            while True:
                frame = self.audio_queue.get()
                current_time = time.time()
                if not self.sound_detected(frame):
                    # Vérifie si le temps minimal d'enregistrement de 3 secondes est écoulé
                    if current_time - self.start_time > 3:
                        break
                audio_data.append(frame)
            audio_data = np.concatenate(audio_data, axis=0)
            print("Enregistrement terminé.")
            return audio_data

    def sound_detected(self, indata):
        """Détermine si du son est détecté dans l'audio."""
        volume_norm = np.linalg.norm(indata) * 10
        return volume_norm > self.threshold

    def save_audio(self, audio_data, file_path="temp_audio.wav"):
        write(file_path, self.rate, audio_data)
        print(f"Audio sauvegardé sous : {file_path}")
        return file_path
