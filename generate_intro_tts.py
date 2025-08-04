#!/usr/bin/env python3
"""
Generate TTS audio files for the new introduction script
"""

import os
import json
from google.cloud import texttospeech
import subprocess

# Initialize the TTS client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ltctraining-b3b3e6e4eb5b.json'
client = texttospeech.TextToSpeechClient()

def generate_tts(text, output_filename):
    """Generate TTS audio for given text"""
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Chirp3-HD-Leda",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.9,
        pitch=0.0
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    
    print(f"Generated: {output_filename}")

def main():
    """Generate all introduction audio files"""
    
    # Introduction scripts
    intro_scripts = [
        ("Hello and welcome! Our job in the Traffic Department at CBS Sports Network is to represent Advertisers and ensure that their Commercials make it to air. Covering live traffic means you will be monitoring commercial inventory in real time while ensuring that airing criteria and network guidelines are met. In other words, you will be watching different sporting events and making sure the commercials are shown on television according to a specific set of rules. Don't worry! We will learn all about Commercials and the rules for airing them in the course.", "static/audio/introduction/intro_01.mp3"),
        ("Before we begin, here are a few basic terms to familiarize yourself with:", "static/audio/introduction/intro_02.mp3"),
        ("Advertiser: An individual or organization that promotes products, services, or ideas to a target audience.", "static/audio/introduction/intro_03.mp3"),
        ("Commercial: A short advertisement that promotes a product or service.", "static/audio/introduction/intro_04.mp3"),
        ("Unit: Another word for Commercial. These terms are used interchangeably in the Traffic Department.", "static/audio/introduction/intro_05.mp3"),
        ("Commercial Breaks: The planned intervals during which advertisements are aired.", "static/audio/introduction/intro_06.mp3"),
        ("Window: A term used in the Traffic Department for any particular program or game. Window refers specifically to the time period during which the program or game airs, encompassing the duration from its beginning to its end. For example, instead of saying 7 PM Basketball Game, we would say 7 PM Window.", "static/audio/introduction/intro_07.mp3"),
        ("Live Coverage Sheet: An excel spreadsheet containing all the vital information you will need in order to properly air Commercials or Units.", "static/audio/introduction/intro_08.mp3"),
        ("Swaps: The word for making changes on the live coverage sheet. It typically involves saving or updating a commercial unit. This process includes modifying the placement of commercials during live broadcasts to align with the timing or logistics, to ensure accurate tracking and smooth execution of the broadcast. Essentially, swaps are quick adjustments made in real-time to the coverage sheet to manage commercial placements effectively.", "static/audio/introduction/intro_09.mp3"),
        ("Dead: A term used in the Traffic Department to indicate that a Commercial or Unit will not air at all that day or night.", "static/audio/introduction/intro_10.mp3"),
        ("CUT: A term used when a Commercial or Unit has been removed from its original spot. A CUT Commercial or Unit may still air in another show or time slot. Note: While Dead and Cut are sometimes used interchangeably, they do not mean exactly the same thing. A dead unit never airs, while a cut unit might.", "static/audio/introduction/intro_11.mp3"),
        ("What is live coverage?", "static/audio/introduction/intro_12.mp3"),
        ("Managing and airing all Commercials or Units during live games.", "static/audio/introduction/intro_13.mp3"),
        ("Communicating with the network producer and Master Control through phone and email. We will refer to Master Control as MC from here on. They are the people that ultimately send the commercials to air. We communicate with them the most. So be nice to them!", "static/audio/introduction/intro_14.mp3"),
        ("Marking down airing times.", "static/audio/introduction/intro_15.mp3"),
        ("Effectively managing inventory is crucial for the financial and overall success of CBS Sports Network. The network operates on a 24-hour clock from 6 AM to 6 AM, so our goal is to schedule and properly organize the Commercials within that 24-hour period!", "static/audio/introduction/intro_16.mp3"),
        ("Beware! There are many factors that contribute to the ever changing schedules of live coverage. A program can go longer than anticipated. As a result, Units can be cut. Our job is to advocate for Commercials or Units and ensure that they air on TV despite these changes.", "static/audio/introduction/intro_17.mp3"),
        ("The role may appear intimidating at first, but don't worry. This training course will set you up for success in the CBS Traffic Department.", "static/audio/introduction/intro_18.mp3"),
        ("Keep in mind there will be practice questions throughout the course, and there will be a test at the end. You must score 70% or higher on the test to proceed.", "static/audio/introduction/intro_19.mp3"),
        ("Participants must take notes and prepare questions for a follow-up appointment with the Traffic Team.", "static/audio/introduction/intro_20.mp3")
    ]
    
    print("Generating introduction TTS audio files...")
    
    for i, (text, output_file) in enumerate(intro_scripts, 1):
        print(f"Generating intro_{i:02d}.mp3...")
        generate_tts(text, output_file)
    
    print("All introduction audio files generated successfully!")

if __name__ == "__main__":
    main() 