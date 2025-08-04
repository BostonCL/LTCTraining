#!/usr/bin/env python3

import re

def add_title_audio_to_file(filename, updates):
    """Add title audio properties to a Svelte file"""
    with open(filename, 'r') as f:
        content = f.read()
    
    for slide_info in updates:
        # Find the slide that needs title audio
        pattern = slide_info['pattern']
        replacement = slide_info['replacement']
        
        # Use regex to find and replace
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            print(f"Added title audio to {filename}")
        else:
            print(f"Could not find pattern in {filename}")
    
    with open(filename, 'w') as f:
        f.write(content)

def main():
    # StandAloneRule.svelte - add title audio to slide 2
    standalone_updates = [
        {
            'pattern': r'(\s+whiteboardText: \[\s+\'Not Allowed:\',\s+\'Allowed:\',\s+\'In this example, the Hershey\'s unit creates the necessary separation between the insurance and alcohol units\.\'\s+\],\s+)image: \'/images/introduction/basketballBackground\.png\'',
            'replacement': r'\1titleAudio: \'/audio/module-3/stand-alone-rule/module3_standalonerule_02_title.mp3\',\n    image: \'/images/introduction/basketballBackground.png\''
        }
    ]
    add_title_audio_to_file('src/routes/mainMenu/module-3/StandAloneRule.svelte', standalone_updates)
    
    # CommercialTimes.svelte - add title audio to slide 1
    commercial_updates = [
        {
            'pattern': r'(\s+whiteboardText: \[\s+\'Write down commercial times\',\s+\'One of our main responsibilities is logging commercial times\.\',\s+\'Track the commercials as they air to make sure they match what\'s on your log sheet\.\',\s+\'If you spot any issues — like a commercial that didn\'t run — you\'ll need to make a swap\.\'\s+\],\s+)image: \'/images/introduction/basketballBackground\.png\'',
            'replacement': r'\1titleAudio: \'/audio/module-3/commercial-times/module3_commercialtimes_01_title.mp3\',\n    image: \'/images/introduction/basketballBackground.png\''
        }
    ]
    add_title_audio_to_file('src/routes/mainMenu/module-3/CommercialTimes.svelte', commercial_updates)
    
    # Module3Intro.svelte - add title audio to slides 3-4
    intro_updates = [
        {
            'pattern': r'(\s+whiteboardText: \[\s+\'Advertiser/Brand Conflicts\',\s+\'Never place competing brands in same break\',\s+\'Ex: Geico & USAA, Lowe\'s & Home Depot\',\s+\'Ask if unsure!\'\s+\]\s+)',
            'replacement': r'\1titleAudio: \'/audio/module-3/intro/module3_intro_03_title.mp3\',\n    '
        },
        {
            'pattern': r'(\s+whiteboardText: \[\s+\'STAND ALONE Rule: Alcohol Ad Placement\',\s+\'Alcohol cannot air before/after auto or insurance\',\s+\'Use other units to separate them\'\s+\]\s+)',
            'replacement': r'\1titleAudio: \'/audio/module-3/intro/module3_intro_04_title.mp3\',\n    '
        }
    ]
    add_title_audio_to_file('src/routes/mainMenu/module-3/Module3Intro.svelte', intro_updates)

if __name__ == "__main__":
    main() 