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
    
    # Combined slides 11 and 12
    combined_text = "Finally, double-check that everything is correct: The local is marked as moved to Break 5 of the 10 PM game. It's noted as moved from Break 11 of the 12 PM game. All cuts, moves, and fills are noted. Your colors are correct: red means cut, blue means airing. And that's how you swap locals! During the game, if things are running smoothly and commercials are airing as planned, start preparing a backup plan in case the game does go over."
    output_file = "static/audio/module-3/local-swaps/module3_localswaps_11_12_combined.mp3"
    generate_tts(combined_text, output_file)

if __name__ == "__main__":
    main() 