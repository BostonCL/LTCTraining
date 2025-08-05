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
    os.makedirs("static/audio/module-2/yellow-unit", exist_ok=True)
    
    # Yellow Unit slide 1 with corrected pronunciation
    # Using "Ordered As" instead of "Ordered A's"
    slide1_text = "Let's start with the basics: The Yellow Unit category. On the next slide, they are listed from most to least important. As you might remember, they are located in the Ordered As column on the live coverage sheet."
    output_file1 = "static/audio/module-2/yellow-unit/module2_yellowunit_01.mp3"
    generate_tts(slide1_text, output_file1)

if __name__ == "__main__":
    main() 