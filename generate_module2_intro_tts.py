from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient.from_service_account_file("ltctraining-b3b3e6e4eb5b.json")

lines = [
    ("One of our main responsibilities is logging commercial times. You’ll need to watch the entire sporting event and track the commercials as they air to make sure they match what’s on your log sheet.",
     "static/audio/module-3/commercial-times/module3_commercialtimes_01.mp3"),
    ("If you spot any issues — like a commercial that didn’t run — you’ll need to make a swap.",
     "static/audio/module-3/commercial-times/module3_commercialtimes_02.mp3"),
]

voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    name="en-US-Chirp3-HD-Leda"
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

for text, output_path in lines:
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to {output_path}") 