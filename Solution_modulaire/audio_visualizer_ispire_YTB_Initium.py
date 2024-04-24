import numpy as np
import pygame
import pyaudio
import math

# Paramètres de configuration pour l'audio
RATE = 44100
CHANNELS = 1
CHUNK = 1024

class AudioVisualizer:
    def __init__(self, rate=RATE, channels=CHANNELS, chunk=CHUNK):
        self.rate = rate
        self.channels = channels
        self.chunk = chunk
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = self.pyaudio_instance.open(
            format=pyaudio.paInt16, 
            channels=self.channels, 
            rate=self.rate, 
            input=True, 
            frames_per_buffer=self.chunk
        )

    def get_microphone_input_level(self, num_samples=CHUNK):
        """Calculates the RMS amplitude of audio data."""
        data = np.frombuffer(self.stream.read(num_samples), dtype=np.int16)
        # Ensure data is not empty or consists only of zeros
        if data.size == 0 or np.all(data == 0):
            return 0  # Return 0 if data is empty or only zeros

        # Calculate the mean of the squared data
        mean_square = np.mean(np.square(data))
        if mean_square <= 0:
            return 0  # Return 0 if mean_square is not positive

        # Calculate RMS
        rms = np.sqrt(mean_square)
        return rms

    def visualize_audio(self):
        """Function to visualize the audio using Pygame."""
        pygame.init()
        screen_width, screen_height = 500, 500
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Neuropal_Visualizer")
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            amplitude = self.get_microphone_input_level() * 2
            if not np.isfinite(amplitude):  # Check if amplitude is finite
                amplitude = 1

            screen.fill((0, 0, 0))
            points = []

            for x in range(screen_width):
                try:
                    y = int(screen_height / 2 + amplitude * math.sin(x * 0.02))
                    points.append((x, y))
                except ValueError as e:
                    print(f"Value error: {e} with amplitude: {amplitude}")
                    continue

            pygame.draw.lines(screen, (255, 255, 255), False, points, 2)
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio_instance.terminate()

    def start_visualization(self):
        """Starts the audio visualization."""
        self.visualize_audio()

if __name__ == "__main__":
    visualizer = AudioVisualizer()
    visualizer.start_visualization()
