#!/usr/bin/env python3

import os
from google.cloud import texttospeech

def generate_tts(text, output_file, voice="en-US-Chirp3-HD-Leda"):
    """Generate TTS audio using Google Cloud Text-to-Speech"""
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice_config = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_config, audio_config=audio_config
    )
    
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    
    print(f"Generated: {output_file}")

def main():
    # Create directory if it doesn't exist
    os.makedirs("static/audio/module-3/local-swaps", exist_ok=True)
    
    # Slide 11
    slide11_text = "After you insert the local: In your spreadsheet, mark it as \"No fill\"."
    output_file11 = "static/audio/module-3/local-swaps/module3_localswaps_12.mp3"
    generate_tts(slide11_text, output_file11)

if __name__ == "__main__":
    main() 