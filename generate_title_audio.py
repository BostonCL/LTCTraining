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
    # Title texts for introduction slides
    titles = {
        'intro_03_title.mp3': 'Advertiser',
        'intro_04_title.mp3': 'Commercial',
        'intro_05_title.mp3': 'Unit',
        'intro_06_title.mp3': 'Commercial Breaks',
        'intro_07_title.mp3': 'Window',
        'intro_08_title.mp3': 'Live Coverage Sheet',
        'intro_09_title.mp3': 'Swaps',
        'intro_10_title.mp3': 'Dead',
        'intro_11_title.mp3': 'CUT',
        'intro_12_title.mp3': 'What is live coverage?'
    }
    
    # Create output directory if it doesn't exist
    output_dir = 'static/audio/introduction'
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate TTS for each title
    for filename, text in titles.items():
        output_path = os.path.join(output_dir, filename)
        generate_tts(text, output_path)

if __name__ == "__main__":
    main() 