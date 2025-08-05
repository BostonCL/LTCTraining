#!/usr/bin/env python3
"""
Generate TTS audio files for the new introduction script
"""

import os
import json
from google.cloud import texttospeech
import subprocess

# Initialize the TTS client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ltctraining-b3b3e6e4eb5b.json'
client = texttospeech.TextToSpeechClient()

def generate_tts(text, output_filename):
    """Generate TTS audio for given text"""
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Chirp3-HD-Leda",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.9,
        pitch=0.0
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    
    print(f"Generated: {output_filename}")

def main():
    """Generate CUT audio file with correct pronunciation"""
    
    # Only generate the CUT audio (intro_11.mp3)
    cut_text = "Cut is a term used when a Commercial or Unit has been removed from its original spot. A Cut Commercial or Unit may still air in another show or time slot. Note: While Dead and Cut are sometimes used interchangeably, they do not mean exactly the same thing. A dead unit never airs, while a cut unit might."
    
    print("Regenerating CUT audio with correct pronunciation...")
    generate_tts(cut_text, "static/audio/introduction/intro_11.mp3")
    print("CUT audio regenerated successfully!")

if __name__ == "__main__":
    main() 