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
    
    # New slide 12 text
    slide12_text = "Effectively managing inventory is crucial for the financial and overall success of CBS Sports Network. The network operates on a 24-hour clock from 6 AM to 6 AM, so our goal is to schedule and properly organize the commercials within that 24-hour period! Beware! There are many factors that contribute to the ever changing schedules of live coverage. A program can go longer than anticipated. As a result, Units can be cut. Our job is to advocate for Commercials or Units and ensure that they air on TV despite these changes. The role may appear intimidating at first, but don't worry. This training course will set you up for success in the CBS Traffic Department. Keep in mind there will be practice questions throughout the course, and there will be a test at the end. You must score 70% or higher on the test to proceed. Participants must take notes and prepare questions for a follow-up appointment with the Traffic Team."
    output_file = "static/audio/introduction/intro_12_13_14_15_16_combined.mp3"
    generate_tts(slide12_text, output_file)
    
    print("Slide 12 audio generated successfully!")

if __name__ == "__main__":
    main() 