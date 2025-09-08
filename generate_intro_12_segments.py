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
    os.makedirs("static/audio/introduction", exist_ok=True)
    
    # Generate the three audio segments for "What is live coverage?" slide
    segment1_text = "Managing and airing all Commercials/Units during live games."
    output_file1 = "static/audio/introduction/intro_12_segment1.mp3"
    generate_tts(segment1_text, output_file1)
    
    segment2_text = "Communicating with the network producer and Master Control through phone and email. We will refer to Master Control as MC from here on. They are the people that ultimately send the commercials to air. We communicate with them the most. So be nice to them!"
    output_file2 = "static/audio/introduction/intro_12_segment2.mp3"
    generate_tts(segment2_text, output_file2)
    
    segment3_text = "Marking down airing times."
    output_file3 = "static/audio/introduction/intro_12_segment3.mp3"
    generate_tts(segment3_text, output_file3)
    
    print("\nAll audio segments generated successfully!")

if __name__ == "__main__":
    main()
