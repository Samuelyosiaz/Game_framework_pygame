
import tempfile
import math
import struct
import wave
import arcade
from pathlib import Path

# Sound settings
SOUND_VOLUME = 0.60
SAMPLE_RATE = 22050

class SoundManager:
    """Generate and manage game sound effects."""

    def __init__(self):
        # Keep generated audio files available during the game.
        self.sound_directory = tempfile.TemporaryDirectory()
        self.sounds = {}

        self.create_sounds()

    def generate_sound(self, name, notes):
        """
        Generate a WAV file using a sequence of notes.
        Each note contains a frequency and a duration.
        """
        file_path = (
            Path(self.sound_directory.name) / f"{name}.wav"
        )

        samples = []

        for frequency, duration in notes:
            sample_count = int(SAMPLE_RATE * duration)

            for i in range(sample_count):
                time = i / SAMPLE_RATE

                # Apply an envelope to prevent sharp audio clicks.
                attack = min(1.0, time / 0.008)
                release = min(
                    1.0,
                    (duration - time) / 0.035
                )

                envelope = max(
                    0.0,
                    min(attack, release)
                )

                # Combine two waves for a retro game sound.
                primary_wave = math.sin(
                    2 * math.pi * frequency * time
                )

                secondary_wave = 0.20 * math.sin(
                    2 * math.pi * frequency * 2 * time
                )

                value = (
                    (primary_wave + secondary_wave)
                    * envelope
                    * 0.55
                )

                value = max(-1.0, min(1.0, value))

                samples.append(int(value * 32767))

        with wave.open(str(file_path), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(SAMPLE_RATE)

            audio_data = struct.pack(
                f"<{len(samples)}h",
                *samples
            )

            wav_file.writeframes(audio_data)

        self.sounds[name] = arcade.load_sound(
            str(file_path),
            streaming=False
        )

    def create_sounds(self):
        """Create five different game sound effects."""

        # Short high-pitched sound for brick collisions.
        self.generate_sound(
            "brick",
            [(780, 0.055), (1040, 0.065)]
        )

        # Soft sound for wall collisions.
        self.generate_sound(
            "wall",
            [(380, 0.065)]
        )

        # Stronger sound for paddle collisions.
        self.generate_sound(
            "paddle",
            [(300, 0.07), (470, 0.07)]
        )

        # Ascending melody for winning.
        self.generate_sound(
            "win",
            [
                (523, 0.14),
                (659, 0.14),
                (784, 0.14),
                (1047, 0.35)
            ]
        )

        # Descending melody for losing.
        self.generate_sound(
            "lose",
            [
                (440, 0.20),
                (349, 0.20),
                (262, 0.25),
                (196, 0.40)
            ]
        )

    def play(self, name):
        """Play a sound effect by its name."""
        sound = self.sounds.get(name)

        if sound is not None:
            arcade.play_sound(
                sound,
                volume=SOUND_VOLUME
            )