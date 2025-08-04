#!/usr/bin/env python3
"""
Generate TTS audio file for Hit Time single script
"""

from google.cloud import texttospeech
import os

# Set up client (ensure GOOGLE_APPLICATION_CREDENTIALS is set or pass credentials here)
client = texttospeech.TextToSpeechClient.from_service_account_file("ltctraining-b3b3e6e4eb5b.json")

# Define the Hit Time single script
hit_time_script = {
    "text": "Right next door is the Hit Time column, this will determine a Mock Schedule. We use Mock Schedules for planning placement of Commercials. Hit Times are not the actual times that commercials air, just estimated placeholders. This column is very important when moving Units around because of a rule called 'Brand SEP.' Brand SEP will be discussed further in Module 3.",
    "output_path": "static/audio/module-1/03-hit-time/module1_hittime_single.mp3"
}

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
os.makedirs("static/audio/module-1/03-hit-time", exist_ok=True)

# Generate audio for the script
print(f"\n--- Generating Hit Time Single Script ---")
print(f"Text: {hit_time_script['text']}")
print(f"Output: {hit_time_script['output_path']}")

# Set the synthesis input
synthesis_input = texttospeech.SynthesisInput(text=hit_time_script['text'])

# Perform the text-to-speech request
response = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)

# Save the output as an MP3 file
with open(hit_time_script['output_path'], "wb") as out:
    out.write(response.audio_content)
    print(f"✅ Audio content written to {hit_time_script['output_path']}")

print(f"\n🎉 Hit Time single audio file generated successfully!")
print(f"\nGenerated file:")
print(f"  - {hit_time_script['output_path']}") 