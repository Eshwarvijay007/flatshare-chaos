from __future__ import annotations
import os
import sounddevice as sd
import numpy as np
from piper.voice import PiperVoice

# --- Voice Model Management ---
VOICE_MAP = {
    "Corporate Carl": "en_US-lessac-medium.onnx",
    "Party Pete": "en_US-ryan-medium.onnx",
    "Ghost Gina": "en_GB-semaine-medium.onnx",
    "Lo-fi Luna": "en_US-ljspeech-medium.onnx",
    "Prepper Priya": "en_GB-alan-low.onnx",
    # Add mappings for other personalities as you download models
    "CodeMaster": "en_US-lessac-medium.onnx",
    "SavageBurn": "en_US-ryan-medium.onnx",
    "UncleJi": "en_GB-alan-low.onnx",
    "ChefCritic": "en_GB-semaine-medium.onnx",
    "BeatDrop": "en_US-ryan-medium.onnx",
    "ChaosKing": "en_US-lessac-medium.onnx",
    "QuietStorm": "en_US-ljspeech-medium.onnx",
    "PennyPincher": "en_GB-alan-low.onnx",
    "DeepThought": "en_GB-semaine-medium.onnx",
}

class AudioManager:
    """Manages loading Piper TTS models and playing audio."""

    def __init__(self, model_dir: str = "models/piper"):
        self.voices = {}
        self.model_dir = model_dir
        print("Audio Manager: Initializing voices...")
        self._load_voices()

    def _load_voices(self):
        """Load all voice models defined in VOICE_MAP."""
        if not os.path.isdir(self.model_dir):
            print(f"Warning: Voice model directory not found at '{self.model_dir}'")
            print("Please download Piper models to enable voice.")
            return

        for name, model_file in VOICE_MAP.items():
            model_path = os.path.join(self.model_dir, model_file)
            if os.path.exists(model_path):
                try:
                    self.voices[name] = PiperVoice.load(model_path)
                    print(f"  - Loaded voice for: {name}")
                except Exception as e:
                    print(f"Error loading voice for {name}: {e}")
            else:
                print(f"  - Model file not found for {name}: {model_path}")
        
        if not self.voices:
            print("No voice models were loaded. Voice output will be disabled.")

    def say(self, text: str, character_name: str):
        """Synthesize and play audio for a given character."""
        if character_name not in self.voices:
            return

        voice = self.voices[character_name]

        try:
            # Collect audio chunks from Piper synthesize method
            audio_arrays = []
            for audio_chunk in voice.synthesize(text):
                # Use the int16 array directly from each chunk
                int16_array = audio_chunk.audio_int16_array
                audio_arrays.append(int16_array)
            
            if audio_arrays:
                # Concatenate all chunks into a single array
                full_audio = np.concatenate(audio_arrays)
                
                # Play the audio using sounddevice
                sd.play(full_audio, voice.config.sample_rate)
                sd.wait()  # Wait for playback to complete
            else:
                print(f"Warning: No audio data generated for {character_name}")
                
        except Exception as e:
            print(f"Error playing audio for {character_name}: {e}")
