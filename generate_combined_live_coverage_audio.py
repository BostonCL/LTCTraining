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
    
    # Combined live coverage text
    combined_text = "What is live coverage? Live coverage involves three main responsibilities: Managing and airing all Commercials or Units during live games. Communicating with the network producer and Master Control through phone and email. We will refer to Master Control as MC from here on. They are the people that ultimately send the commercials to air. We communicate with them the most. So be nice to them! And marking down airing times."
    output_file = "static/audio/introduction/intro_12_13_14_15_combined.mp3"
    generate_tts(combined_text, output_file)
    
    print("Combined live coverage audio generated successfully!")

if __name__ == "__main__":
    main() 