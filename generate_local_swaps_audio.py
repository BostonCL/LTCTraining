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
    
    # Slide 9
    slide9_text = "Add a note that says: 'Moved to Break 5 of the 10 PM game.'"
    output_file9 = "static/audio/module-3/local-swaps/module3_localswaps_10.mp3"
    generate_tts(slide9_text, output_file9)
    
    # Slide 10
    slide10_text = "Add a note that says: 'Moved from Break 11 of the 12 PM game.'"
    output_file10 = "static/audio/module-3/local-swaps/module3_localswaps_11.mp3"
    generate_tts(slide10_text, output_file10)

if __name__ == "__main__":
    main() 