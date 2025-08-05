# Regenerate CUT Audio

The audio for slide 10 (CUT definition) currently says "c-HUT" instead of "Cut". To fix this, you need to regenerate the audio file.

## Prerequisites

You need the Google Cloud credentials file: `ltctraining-b3b3e6e4eb5b.json`

## Steps to Regenerate

1. **Place the credentials file** in the project root directory:
   ```
   /Users/bostonlearned/LTCTraining/ltctraining-b3b3e6e4eb5b.json
   ```

2. **Run the regeneration script**:
   ```bash
   python3 generate_intro_tts.py
   ```

3. **Verify the fix**:
   - The script will regenerate `static/audio/introduction/intro_11.mp3`
   - The new audio should pronounce "CUT" correctly instead of "c-HUT"

## Alternative: Manual Fix

If you don't have the credentials file, you can:

1. **Use the existing script** `generate_cut_audio_fix.py` (already created)
2. **Add the credentials file** to the project root
3. **Run**: `python3 generate_cut_audio_fix.py`

## Expected Result

The audio should now say "Cut is a term used when..." instead of "CUT: A term used when..." and pronounce "Cut" correctly (rhyming with "but") instead of "c-HUT" (rhyming with "hut").

## Text Change

The text has been updated from:
- **Old**: "CUT: A term used when..."
- **New**: "Cut is a term used when..."

## File Location

The audio file is located at:
```
static/audio/introduction/intro_11.mp3
```

This corresponds to slide 10 in the introduction, which defines the term "CUT". 