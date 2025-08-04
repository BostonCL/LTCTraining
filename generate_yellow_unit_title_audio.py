#!/usr/bin/env python3

import os
import sys
from google.cloud import texttospeech

# Add the path to the credentials file
sys.path.append('/Users/bostonlearned/LTCTraining')

# Set up Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ltctraining-b3b3e6e4eb5b.json'

def generate_tts(text, output_filename):
    """Generate TTS audio for the given text"""
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Chirp3-HD-Leda",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.9
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    
    print(f"Generated: {output_filename}")

def main():
    # Create output directory
    os.makedirs("static/audio/module-2/green-purple-units", exist_ok=True)
    
    # Title text for each slide
    title_texts = [
        "Purple & Green Units",  # Slide 2
        "Locals",               # Slide 4
        "DRs (Direct Response)", # Slide 5
        "Promos",               # Slide 6
        "PSAs"                  # Slide 7
    ]
    
    # Generate title audio for slides 2, 4-7
    slide_numbers = [2, 4, 5, 6, 7]
    for i, title_text in zip(slide_numbers, title_texts):
        output_file = f"static/audio/module-2/green-purple-units/module2_greenpurpleunits_{i:02d}_title.mp3"
        generate_tts(title_text, output_file)

if __name__ == "__main__":
    main() 