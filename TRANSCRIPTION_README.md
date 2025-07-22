# Video Transcription with OpenAI Whisper

This script uses OpenAI's Whisper model to transcribe MP4 video files to text.

## Installation

Whisper has been installed via pip. The script is ready to use!

## Usage

### Transcribe a single video file:
```bash
python3 transcribe_videos.py /path/to/your/video.mp4
```

### Transcribe all MP4 files in a directory:
```bash
python3 transcribe_videos.py /path/to/video/directory
```

### Save transcriptions to a specific output directory:
```bash
python3 transcribe_videos.py /path/to/video.mp4 -o /path/to/output/directory
```

### Use a different Whisper model (for better accuracy):
```bash
python3 transcribe_videos.py /path/to/video.mp4 -m medium
```

## Model Options

- `tiny`: Fastest, least accurate
- `base`: Good balance of speed and accuracy (default)
- `small`: Better accuracy, slower
- `medium`: High accuracy, slower
- `large`: Best accuracy, slowest

## Examples

1. **Transcribe a single video:**
   ```bash
   python3 transcribe_videos.py ~/Videos/my_video.mp4
   ```

2. **Transcribe all videos in a folder:**
   ```bash
   python3 transcribe_videos.py ~/Videos/
   ```

3. **Use high-quality model and save to specific folder:**
   ```bash
   python3 transcribe_videos.py ~/Videos/my_video.mp4 -m medium -o ~/Desktop/transcriptions
   ```

## Output

The script creates a text file with the transcription in the same directory as the video (or in the specified output directory). The filename will be `[original_filename]_transcription.txt`.

## Notes

- The first time you run the script, it will download the Whisper model (this may take a few minutes)
- Larger models provide better accuracy but take longer to process
- The script supports any MP4 video file
- Transcriptions are saved as UTF-8 text files 