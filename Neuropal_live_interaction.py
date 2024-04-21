import speech_recognition as sr
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write
import os
import whisper
from openai import OpenAI

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech speed

# Initialize the Whisper model for STT
model = whisper.load_model("medium")

# Initialize the LLM client
client = OpenAI(base_url="http://localhost:4444/v1", api_key="lm-studio")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def audio_to_text(audio, fs):
    audio_path = "temp_audio.wav"
    write(audio_path, fs, audio)  # Save the audio temporarily
    result = model.transcribe(audio_path)
    os.remove(audio_path)  # Delete the temporary audio file
    return result['text']

def get_response(text):
    history = [
        {"role": "system", "content": "You are an intelligent assistant."},
        {"role": "user", "content": text},
    ]
    completion = client.chat.completions.create(
        model="NousResearch/Hermes-2-Pro-Mistral-7B-GGUF/Hermes-2-Pro-Mistral-7B.Q4_0.gguf",
        messages=history,
        temperature=0.7,
    )
    return completion.choices[0].message.content

def record_audio(seconds=10):
    fs = 44100
    print("Recording...")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    print("Recording finished.")
    return recording, fs

def listen_for_keyword(keyword="amorcer"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print(f"Listening for the keyword '{keyword}'...")
        audio = r.listen(source)
        try:
            said = r.recognize_google(audio, language="fr-FR")
            print("Heard:", said)
            return said.lower() == keyword.lower()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        return False

def main():
    while True:
        if listen_for_keyword():
            speak("J'ai entendu le mot clé, je vous écoute maintenant.")
            audio, fs = record_audio()
            text = audio_to_text(audio, fs)
            print("Transcription:", text)
            
            # Check if "Neutraliser" was said to interrupt and restart listening
            if "neutraliser" in text:
                print("Commande 'Neutraliser' détectée. La synthèse vocale est désactivée.")
                continue
            
            response = get_response(text)
            print("Réponse:", response)
            speak(response)

if __name__ == "__main__":
    main()
