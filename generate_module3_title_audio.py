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
    # Module 3 Intro
    os.makedirs("static/audio/module-3/intro", exist_ok=True)
    intro_titles = [
        "Brand SEP",
        "Advertiser/Brand Conflicts", 
        "STAND ALONE Rule: Alcohol Ad Placement"
    ]
    for i, title in enumerate(intro_titles, 2):
        output_file = f"static/audio/module-3/intro/module3_intro_{i:02d}_title.mp3"
        generate_tts(title, output_file)

    # Brand SEP
    os.makedirs("static/audio/module-3/brand-sep", exist_ok=True)
    brandsep_titles = [
        "Brand SEP",
        "Additional Guidelines",
        "Exceptions"
    ]
    for i, title in enumerate(brandsep_titles, 1):
        output_file = f"static/audio/module-3/brand-sep/module3_brandsep_{i:02d}_title.mp3"
        generate_tts(title, output_file)

    # Advertiser Conflicts
    os.makedirs("static/audio/module-3/advertiser-conflicts", exist_ok=True)
    advertiser_titles = [
        "Advertiser Conflicts also known as Brand Conflicts",
        "For example:",
        "If you're unsure",
        "Why this matters:"
    ]
    for i, title in enumerate(advertiser_titles, 1):
        output_file = f"static/audio/module-3/advertiser-conflicts/module3_advertiserconflicts_{i:02d}_title.mp3"
        generate_tts(title, output_file)

    # Stand Alone Rule
    os.makedirs("static/audio/module-3/stand-alone-rule", exist_ok=True)
    standalone_titles = [
        "STAND ALONE Rule: Alcohol Ad Placement",
        "Not Allowed:"
    ]
    for i, title in enumerate(standalone_titles, 1):
        output_file = f"static/audio/module-3/stand-alone-rule/module3_standalonerule_{i:02d}_title.mp3"
        generate_tts(title, output_file)

    # Commercial Times
    os.makedirs("static/audio/module-3/commercial-times", exist_ok=True)
    commercial_titles = [
        "Write down commercial times"
    ]
    for i, title in enumerate(commercial_titles, 1):
        output_file = f"static/audio/module-3/commercial-times/module3_commercialtimes_{i:02d}_title.mp3"
        generate_tts(title, output_file)

if __name__ == "__main__":
    main() 