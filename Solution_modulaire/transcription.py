# transcription.py
import whisper
import os

class AudioTranscriber:
    def __init__(self, model_type="medium", device="cuda"):
        self.model = whisper.load_model(model_type, device=device)

    def audio_to_text(self, file_path):
        result = self.model.transcribe(file_path)
        os.remove(file_path)
        return result['text']
