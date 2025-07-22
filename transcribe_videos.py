#!/usr/bin/env python3
"""
Video Transcription Script using OpenAI Whisper
This script helps transcribe MP4 video files to text.
"""

import os
import sys
import whisper
import argparse
from pathlib import Path

def transcribe_video(video_path, output_dir=None, model_size="base"):
    """
    Transcribe a single video file using Whisper.
    
    Args:
        video_path (str): Path to the video file
        output_dir (str): Directory to save transcription files (optional)
        model_size (str): Whisper model size (tiny, base, small, medium, large)
    
    Returns:
        str: Path to the transcription file
    """
    try:
        # Load the Whisper model
        print(f"Loading Whisper model: {model_size}")
        model = whisper.load_model(model_size)
        
        # Get the video file path
        video_file = Path(video_path)
        if not video_file.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        print(f"Transcribing: {video_file.name}")
        
        # Transcribe the video
        result = model.transcribe(str(video_file))
        
        # Determine output directory
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
        else:
            output_path = video_file.parent
        
        # Save transcription to file
        transcription_file = output_path / f"{video_file.stem}_transcription.txt"
        
        def format_timestamp(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            return f"{hours:02}:{minutes:02}:{secs:02}"
        
        with open(transcription_file, 'w', encoding='utf-8') as f:
            f.write(f"Transcription of: {video_file.name}\n")
            f.write("=" * 50 + "\n\n")
            # Write each segment with timestamps
            for segment in result.get("segments", []):
                start = format_timestamp(segment["start"])
                end = format_timestamp(segment["end"])
                text = segment["text"].strip()
                f.write(f"[{start} --> {end}] {text}\n")
        
        print(f"Transcription saved to: {transcription_file}")
        return str(transcription_file)
        
    except Exception as e:
        print(f"Error transcribing {video_path}: {str(e)}")
        return None

def transcribe_directory(input_dir, output_dir=None, model_size="base"):
    """
    Transcribe all MP4 files in a directory.
    
    Args:
        input_dir (str): Directory containing MP4 files
        output_dir (str): Directory to save transcription files
        model_size (str): Whisper model size
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"Directory not found: {input_dir}")
        return
    
    # Find all MP4 files
    mp4_files = list(input_path.glob("*.mp4"))
    
    if not mp4_files:
        print(f"No MP4 files found in: {input_dir}")
        return
    
    print(f"Found {len(mp4_files)} MP4 files to transcribe")
    
    for video_file in mp4_files:
        print(f"\nProcessing: {video_file.name}")
        transcribe_video(str(video_file), output_dir, model_size)

def main():
    parser = argparse.ArgumentParser(description="Transcribe MP4 videos using OpenAI Whisper")
    parser.add_argument("input", help="Path to video file or directory")
    parser.add_argument("-o", "--output", help="Output directory for transcriptions")
    parser.add_argument("-m", "--model", default="base", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Whisper model size (default: base)")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        # Transcribe single file
        if input_path.suffix.lower() != '.mp4':
            print("Error: Input must be an MP4 file")
            sys.exit(1)
        transcribe_video(str(input_path), args.output, args.model)
    
    elif input_path.is_dir():
        # Transcribe all MP4 files in directory
        transcribe_directory(str(input_path), args.output, args.model)
    
    else:
        print(f"Error: {args.input} is not a valid file or directory")
        sys.exit(1)

if __name__ == "__main__":
    main() 