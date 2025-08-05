#!/usr/bin/env python3

import os
from google.cloud import texttospeech

def generate_tts(text, output_file, voice="en-US-Chirp3-HD-Leda"):
    """Generate TTS audio using Google Cloud Text-to-Speech"""
    # Set up credentials
    import os
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ltctraining-b3b3e6e4eb5b.json'
    
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
    os.makedirs("static/audio/introduction", exist_ok=True)
    
    # CUT definition with correct pronunciation
    cut_text = "Cut is a term used when a Commercial or Unit has been removed from its original spot. A Cut Commercial or Unit may still air in another show or time slot. Note: While Dead and Cut are sometimes used interchangeably, they do not mean exactly the same thing. A dead unit never airs, while a cut unit might."
    output_file = "static/audio/introduction/intro_11.mp3"
    generate_tts(cut_text, output_file)
    
    print("CUT audio regenerated with correct pronunciation!")

if __name__ == "__main__":
    main() 