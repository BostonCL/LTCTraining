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
    # Title texts for Module 2 slides
    titles = {
        # Module 2 main page
        'module2_01_part2_title.mp3': 'YELLOW',
        'module2_01_part3_title.mp3': 'PURPLE',
        'module2_01_part4_title.mp3': 'GREEN',
        
        # TheYellowUnit
        'module2_yellowunit_02_title.mp3': 'Unit Prioritization List',
        'module2_yellowunit_03_title.mp3': 'Show Specific',
        'module2_yellowunit_04_title.mp3': 'Sports Spectacular',
        'module2_yellowunit_05_title.mp3': 'ROS 24 Hour',
        'module2_yellowunit_06_title.mp3': 'ROS Prime',
        'module2_yellowunit_07_title.mp3': 'Studio Encore Sports Encore',
        
        # UnitPrioritizationDetails
        'module2_unitprioritizationdetails_02_title.mp3': 'Show Specific',
        'module2_unitprioritizationdetails_03_title.mp3': 'Sports Spectacular',
        'module2_unitprioritizationdetails_04_title.mp3': 'ROS 24 Hour',
        'module2_unitprioritizationdetails_05_title.mp3': 'ROS Prime',
        'module2_unitprioritizationdetails_06_title.mp3': 'Studio Encore Sports Encore',
        
        # GreenPurpleUnits
        'module2_greenpurpleunits_02_title.mp3': 'Purple and Green Units',
        'module2_greenpurpleunits_04_title.mp3': 'Locals',
        'module2_greenpurpleunits_05_title.mp3': 'DRs Direct Response',
        'module2_greenpurpleunits_06_title.mp3': 'Promos',
        'module2_greenpurpleunits_07_title.mp3': 'PSAs',
        
        # SellingTitle
        'module2_sellingtitle_02_title.mp3': 'Selling Title'
    }
    
    # Create output directories if they don't exist
    directories = [
        'static/audio/module-2/01-intro',
        'static/audio/module-2/yellow-unit',
        'static/audio/module-2/unit-prioritization-details',
        'static/audio/module-2/green-purple-units',
        'static/audio/module-2/selling-title'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Generate TTS for each title
    for filename, text in titles.items():
        # Determine the correct directory based on the filename
        if '01_part' in filename:
            output_dir = 'static/audio/module-2/01-intro'
        elif 'yellowunit' in filename:
            output_dir = 'static/audio/module-2/yellow-unit'
        elif 'unitprioritization' in filename:
            output_dir = 'static/audio/module-2/unit-prioritization-details'
        elif 'greenpurple' in filename:
            output_dir = 'static/audio/module-2/green-purple-units'
        elif 'sellingtitle' in filename:
            output_dir = 'static/audio/module-2/selling-title'
        else:
            output_dir = 'static/audio/module-2'
        
        output_path = os.path.join(output_dir, filename)
        generate_tts(text, output_path)

if __name__ == "__main__":
    main() 