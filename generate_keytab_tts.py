#!/usr/bin/env python3
"""
Generate TTS audio files for Key Tab module
"""

from google.cloud import texttospeech
import os

# Set up client (ensure GOOGLE_APPLICATION_CREDENTIALS is set or pass credentials here)
client = texttospeech.TextToSpeechClient.from_service_account_file("ltctraining-b3b3e6e4eb5b.json")

# Define the Key Tab scripts with their text and output file paths
keytab_scripts = [
    {
        "text": "In the bottom left-hand corner of this Excel file, you'll see two tabs: 'Key' and 'Coverage.' All that we have discussed so far is found in the Coverage tab. You'll spend most of your time working in the Coverage tab, but occasionally you'll need to refer to the Key tab. Keep in mind that some information on the Key tab is outdated, so focus only on the important information explained here.",
        "output_path": "static/audio/module-1/keytab/keytab_01.mp3"
    },
    {
        "text": "Contingency Plan: This plan outlines what to do if a game runs long — for example, which shows might be cut or adjusted.",
        "output_path": "static/audio/module-1/keytab/keytab_02.mp3"
    },
    {
        "text": "Live Coverage Reports: At the end of your shift, you will send out a Live Coverage Report. The list of email recipients is listed below the Live Coverage Reports section.",
        "output_path": "static/audio/module-1/keytab/keytab_03.mp3"
    },
    {
        "text": "One more thing to note: at the top of the sheet, you'll see a color code. The important colors to remember are: Yellow (Commercial), Red (CUT), Blue (Moved From). There will be more information about these color codes and their significance in Module 3.",
        "output_path": "static/audio/module-1/keytab/keytab_04.mp3"
    }
]

# Set the voice parameters
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Chirp3-HD-Leda"
)

# Set the audio configuration
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Create the directory structure if it doesn't exist
os.makedirs("static/audio/module-1/keytab", exist_ok=True)

# Generate audio for each script
for i, script in enumerate(keytab_scripts, 1):
    print(f"\n--- Generating Key Tab Script {i} ---")
    print(f"Text: {script['text']}")
    print(f"Output: {script['output_path']}")
    
    # Set the synthesis input
    synthesis_input = texttospeech.SynthesisInput(text=script['text'])
    
    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    # Save the output as an MP3 file
    with open(script['output_path'], "wb") as out:
        out.write(response.audio_content)
        print(f"✅ Audio content written to {script['output_path']}")

print(f"\n🎉 All {len(keytab_scripts)} Key Tab audio files generated successfully!")
print("\nGenerated files:")
for script in keytab_scripts:
    print(f"  - {script['output_path']}") 