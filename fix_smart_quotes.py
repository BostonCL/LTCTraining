#!/usr/bin/env python3

import re

def fix_smart_quotes_in_file(filename):
    """Fix smart quotes in a file"""
    with open(filename, 'r') as f:
        content = f.read()
    
    # Replace smart quotes with regular quotes
    content = content.replace('"', '"').replace('"', '"')
    content = content.replace(''', "'").replace(''', "'")
    
    with open(filename, 'w') as f:
        f.write(content)
    
    print(f"Fixed smart quotes in {filename}")

def main():
    files_to_fix = [
        'src/routes/mainMenu/module-3/AdvertiserConflicts.svelte',
        'src/routes/mainMenu/module-3/CommercialTimes.svelte',
        'src/routes/mainMenu/module-3/StandAloneRule.svelte',
        'src/routes/mainMenu/module-3/Module3Intro.svelte'
    ]
    
    for filename in files_to_fix:
        fix_smart_quotes_in_file(filename)

if __name__ == "__main__":
    main() 