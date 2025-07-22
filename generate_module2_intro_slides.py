from google.cloud import texttospeech
import os

# Set up client (ensure GOOGLE_APPLICATION_CREDENTIALS is set or pass credentials here)
client = texttospeech.TextToSpeechClient.from_service_account_file("ltctraining-b3b3e6e4eb5b.json")

# Define the slides with their text and output file paths
slides = [
    {
        "text": "In the Ordered As column you'll see many different types of units. In this module we will go over what they all are. When moving around units this is the first column you will look at.",
        "output_path": "static/audio/module-2/module2_intro.mp3"
    },
    {
        "text": "The sold commercials are color coordinated:",
        "output_path": "static/audio/module-2/01-intro/module2_01_part1.mp3"
    },
    {
        "text": "Sold commercials (the important stuff) are in YELLOW",
        "output_path": "static/audio/module-2/01-intro/module2_01_part2.mp3"
    },
    {
        "text": "Local units are PURPLE",
        "output_path": "static/audio/module-2/01-intro/module2_01_part3.mp3"
    },
    {
        "text": "Anything in GREEN is cuttable and is not mandatory to air, these will be Drs, PSAs and Promos.",
        "output_path": "static/audio/module-2/01-intro/module2_01_part4.mp3"
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
os.makedirs("static/audio/module-2/01-intro", exist_ok=True)

# Generate audio for each slide
for i, slide in enumerate(slides, 1):
    print(f"\n--- Generating Slide {i} ---")
    print(f"Text: {slide['text']}")
    print(f"Output: {slide['output_path']}")
    
    # Set the synthesis input
    synthesis_input = texttospeech.SynthesisInput(text=slide['text'])
    
    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    
    # Save the output as an MP3 file
    with open(slide['output_path'], "wb") as out:
        out.write(response.audio_content)
        print(f"✅ Audio content written to {slide['output_path']}")

print(f"\n🎉 All {len(slides)} audio files generated successfully!")
print("\nGenerated files:")
for slide in slides:
    print(f"  - {slide['output_path']}") 