#!/usr/bin/env python3

import os
import subprocess

def combine_audio_files(input_files, output_file):
    """Combine multiple MP3 files into one using ffmpeg"""
    
    # Create the filter complex string for concatenation
    filter_complex = "concat=n={}:v=0:a=1".format(len(input_files))
    
    # Build the ffmpeg command
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output file if it exists
        '-i', input_files[0],
        '-i', input_files[1], 
        '-i', input_files[2],
        '-filter_complex', filter_complex,
        output_file
    ]
    
    # Run the command
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Successfully created: {output_file}")
    else:
        print(f"Error creating {output_file}: {result.stderr}")

def main():
    # Create directory if it doesn't exist
    os.makedirs("static/audio/module-2", exist_ok=True)
    
    # Input files for slide 2 (slides 3, 4, 5)
    input_files = [
        "static/audio/module-2/01-intro/module2_01_part2.mp3",
        "static/audio/module-2/01-intro/module2_01_part3.mp3",
        "static/audio/module-2/01-intro/module2_01_part4.mp3"
    ]
    
    # Output file
    output_file = "static/audio/module-2/module2_slide2_combined.mp3"
    
    # Check if all input files exist
    missing_files = [f for f in input_files if not os.path.exists(f)]
    if missing_files:
        print(f"Missing files: {missing_files}")
        return
    
    combine_audio_files(input_files, output_file)

if __name__ == "__main__":
    main() 