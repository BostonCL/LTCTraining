from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient.from_service_account_file("ltctraining-b3b3e6e4eb5b.json")

lines = [
    ("One of our main responsibilities is logging commercial times. You’ll need to watch the entire sporting event and track the commercials as they air to make sure they match what’s on your log sheet. If you spot any issues — like a commercial that didn’t run — you’ll need to make a swap.",
     "static/audio/module-3/commercial-times/module3_commercialtimes_01.mp3"),
    ("You’ll also stay on the phone with the producer, and MC, listening for their countdowns. When they reach ‘one,’ you’ll record the exact time the commercial airs. For example, if it airs at 8:05:32, you’ll write down ‘8:05:32,’ as shown on this Live Coverage Sheet.",
     "static/audio/module-3/commercial-times/module3_commercialtimes_02.mp3"),
    ("Usually, if a commercial is going to be cut, they’ll mention it over the phone line and ask for your input on which one should be dropped.",
     "static/audio/module-3/commercial-times/module3_commercialtimes_03.mp3"),
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

# --- SWAPS SUBMODULE TTS ---
swaps_lines = [
    ("Welcome to this section. Where we will learn how to properly swap units within the live coverage sheet.", "static/audio/module-3/swaps/module3_swaps_01.mp3"),
    ("In this section, we'll walk through each step you need to follow to make sure your swaps are accurate and compliant.", "static/audio/module-3/swaps/module3_swaps_02.mp3"),
    ("Let's begin with an example scenario. Suppose we are approaching the end of a game, and the producer requests a thirty-second cut from Break 11.", "static/audio/module-3/swaps/module3_swaps_03.mp3"),
    ("We identify that the Jersey Mike's unit needs to be swapped because This Major League Fishing unit is sold exclusively to the current window and cannot air in any other window for the rest of the day. Since local units can only be moved when the producer specifically requests it, we cannot cut it. This leaves the thirty-second Jersey Mike's unit as the only option to move.", "static/audio/module-3/swaps/module3_swaps_04.mp3"),
    ("Now, let's go through the steps you need to follow.", "static/audio/module-3/swaps/module3_swaps_05.mp3"),
    ("Step 1 is to check the Ordered As column. Here, you confirm the unit type. In this case, it is a sports spec unit, which means it can be moved to the next show.", "static/audio/module-3/swaps/module3_swaps_06.mp3"),
    ("Step 2 is to verify the spot end time. The unit has a 1 AM spot end time. Now keep that in mind when moving it.", "static/audio/module-3/swaps/module3_swaps_07.mp3"),
    ("Step 3 is to check the unit length. This unit is thirty seconds long. Remember to keep brand separation in mind, but also keep in mind that brand separation rules can be broken during a live window.", "static/audio/module-3/swaps/module3_swaps_08.mp3"),
    ("Step 4 is to identify which break to cut the inventory from. Let's look at Break 1 of the 2PM window. Looks like there is 30 seconds of unsold inventory so this is a good option. Note the spot end time. It is valid to move it into the 2 P M window, it is still within its airing period and is sports spec approved.", "static/audio/module-3/swaps/module3_swaps_09.mp3"),
    ("Step 5 is to check for brand conflicts within that identified break. Since Jersey Mike's is a restaurant, you need to make sure there is no other restaurant brand in the new break. If there is no conflict, we can continue.", "static/audio/module-3/swaps/module3_swaps_10.mp3"),
    ("Step 6 is to mark the unit status. When a unit is not airing in a break, highlight it red. Red means that the commercial did not air in that break. It can mean that the unit was cut or that it was moved to another break. This is why it is so important to include clear notes next to it. We recommend making clear notations as you go, to avoid confusion later.", "static/audio/module-3/swaps/module3_swaps_11.mp3"),
    ("Step 7 is to notate the move. Write a note that says: Moved to B one of the 2 P. This means the unit is being moved to Break 1 of the 2 PM window.", "static/audio/module-3/swaps/module3_swaps_12.mp3"),
    ("Step 8 is to make the cut. We found thirty seconds of green (unsold) inventory in Break One. Double-check that there is no brand conflict. Highlight this inventory red and add a note that says CUT next to it.", "static/audio/module-3/swaps/module3_swaps_13.mp3"),
    ("Step 9 is to move the unit. Insert a new line within Break 1 and copy and paste the Jersey Mike's unit into its new position.", "static/audio/module-3/swaps/module3_swaps_14.mp3"),
    ("Step 10 is to finalize the notation. On the line you inserted, write moved from B 11 of the 12 PM. Highlight the unit light blue. Blue means that it aired in this break. At this point, the Jersey Mike's unit is now properly marked on the live coverage sheet.", "static/audio/module-3/swaps/module3_swaps_15.mp3"),
    ("Before we wrap up, here are a few key reminders. Always use clear, consistent color coding. Red means the unit did not air here or was moved. Blue means it aired here.", "static/audio/module-3/swaps/module3_swaps_16.mp3"),
    ("Always double-check for brand conflicts. Document every move you make to avoid mistakes. And keep your notes organized so you can easily track your changes.", "static/audio/module-3/swaps/module3_swaps_17.mp3"),
    ("In the next module, we will learn how to document these adjustments in emails.", "static/audio/module-3/swaps/module3_swaps_18.mp3"),
]

# Uncomment to generate SWAPS audio
for text, output_path in swaps_lines:
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to {output_path}")

# --- END TIME SUBMODULE TTS ---
end_time_lines = [
    ("End Time is the end of each show or game, as soon as the final commercial airs — or when the game ends and transitions to the next program — you'll record the exact end time, down to the second, just like when marking down commercials.", "static/audio/module-1/end-time/module1_endtime_01.mp3"),
]

# Generate End Time TTS
for text, output_path in end_time_lines:
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to {output_path}") 

# --- FLOATERS SUBMODULE TTS ---
floaters_lines = [
    ("Floaters are occasionally seen underneath the end time section— these are extra sold commercial units that need to air during the game. They're especially common during basketball. For example, if a player gets injured and there's a pause in play, you might run a short 30 second floater. If it's a more serious injury, you could run a longer one, by combining Floaters A and B for a full minute.", "static/audio/module-1/floaters/module1_floaters_01.mp3"),
    ("Sometimes a Floater will be added to the end of an existing break, but you'll need to be mindful of brand conflicts (which we will go into depth about in Module 3). In this example, if MC wants to add Floater A to Break 12 (the final break), it cannot because there already is a Honda unit in that break.", "static/audio/module-1/floaters/module1_floaters_02.mp3"),
]

# Generate Floaters TTS
for text, output_path in floaters_lines:
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to {output_path}") 

# --- MASTER CONTROL EMAIL SUBMODULE TTS ---
master_control_email_lines = [
    ("In this section, we are going to learn how to properly document commercial swaps and send them to MC, so they can make the same changes on their end.", "static/audio/module-3/master-control-email/module3_mastercontrol_01.mp3"),
    ("First, always start your email by clearly explaining what swap you're making. For example, you could write: 'Here is the swap to save thirty seconds from break 11 of the 12 PM game.' This lets MC know exactly what you're doing.", "static/audio/module-3/master-control-email/module3_mastercontrol_02.mp3"),
    ("Next, identify where you're moving the spot to. So, you are moving the Jersey Mikes unit to the 2 PM window, just write: '2 PM Game'. Keep it simple and clear.", "static/audio/module-3/master-control-email/module3_mastercontrol_03.mp3"),
    ("Under that, write the specific break you're moving the spot into. In this case: 'Break 1'. This shows exactly where the commercial will go.", "static/audio/module-3/master-control-email/module3_mastercontrol_04.mp3"),
    ("Now, you need to show what's being cut to make room for the new spot. Write: 'CUT' and then paste the house numbers of the commercial or commercials you're removing. Always copy and paste the house numbers directly. This really helps eliminate mistakes.", "static/audio/module-3/master-control-email/module3_mastercontrol_05.mp3"),
    ("Finally, show what you're adding in. Under 'CUT'- write 'IN' and paste the house number of the spot you are moving into that break. In this case, you are saving a Jersey Mike's commercial, so you will paste that house number right there.", "static/audio/module-3/master-control-email/module3_mastercontrol_06.mp3"),
    ("So, your final email should look something like this: 'Here is the swap to save :30 seconds from break 11 of the 12 PM game. 2PM Game Break 1 CUT: [House number being cut] IN: [House number of the Jersey Mike's spot]'", "static/audio/module-3/master-control-email/module3_mastercontrol_07.mp3"),
    ("Before you hit send, always double check your break numbers, your times, and the house numbers. Being clear and accurate helps MC mark everything correctly on their end which keeps our spots running smoothly.", "static/audio/module-3/master-control-email/module3_mastercontrol_08.mp3"),
]

# Generate Master Control Email TTS
for text, output_path in master_control_email_lines:
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to {output_path}")

# --- LOCAL SWAPS SUBMODULE TTS ---
local_swaps_lines = [
    ("In this section, we will learn how to swap local units when a producer requests it. Let's look at an example. Imagine the producer has to cut 2 minutes from the break we're working in. They decide to cut the local unit. Remember — locals are always 1 minute and :30 seconds long. So, they cut the local unit (1 minute and :30 seconds) plus the :30 seconds Jersey Mike's spot. That adds up to exactly 2 minutes cut from the break.", "static/audio/module-3/local-swaps/module3_localswaps_01.mp3"),
    ("Now, that local unit is gone from its original spot — but you can't just leave it like that. You must find a new place in the schedule to air that local unit.", "static/audio/module-3/local-swaps/module3_localswaps_02.mp3"),
    ("Key rules to remember: You must always find swaps for locals. You have to find the exact same amount of time (1 minute and :30 seconds) somewhere else in the schedule. Locals can never air in the same break as another local. They can be in back-to-back breaks, but never together in the same break.", "static/audio/module-3/local-swaps/module3_localswaps_03.mp3"),
    ("Start by looking for cuttable units. I like to check the green inventory — that's usually the easiest to cut. Sometimes I'll go deep into the overnight hours because it's simpler there.", "static/audio/module-3/local-swaps/module3_localswaps_04.mp3"),
    ("Once you find cuttable units: Mark those units as cut (turn them red). This means they won't air in that break anymore. Next, insert a line for the local unit you're moving. Notate everything as you go.", "static/audio/module-3/local-swaps/module3_localswaps_05.mp3"),
    ("In this example, we're moving the local unit into Break 5 of the 10 PM game. When you email MC, update the title to: 'Here are the swaps to save 2 minutes from Break 11 of the 12 PM game.' Note the new location: 10 PM game Break 5 CUT: xxx and xxx IN: 1:30 local, please use a fill list", "static/audio/module-3/local-swaps/module3_localswaps_06.mp3"),
    ("Why does this matter? On the traffic side, these schedules already have sold commercials in place. If you just swap in a local unit without using the fill list, it can conflict with other units, create wrong end times, and worst of all, the commercials may not air correctly — which means we wouldn't get paid for them.", "static/audio/module-3/local-swaps/module3_localswaps_07.mp3"),
    ("Using the fill list keeps everything clean. The local network still gets the promised time, and if there's leftover time, PSAs will run instead. The fill list is just a bunch of PSAs that won't conflict with anything else in the break.", "static/audio/module-3/local-swaps/module3_localswaps_08.mp3"),
    ("Then, paste the local unit into its new spot. Mark it blue to show it's airing there.", "static/audio/module-3/local-swaps/module3_localswaps_09.mp3"),
    ("Add a note that says: 'Moved to Break 5 of the 10 PM game.' 'Moved from Break 11 of the 12 PM game.'", "static/audio/module-3/local-swaps/module3_localswaps_10.mp3"),
    ("After you insert the local: In your spreadsheet, mark it as 'No fill'.", "static/audio/module-3/local-swaps/module3_localswaps_11.mp3"),
    ("Finally, double-check that everything is correct: The local is marked as moved to Break 5 of the 10 PM game. It's noted as moved from Break 11 of the 12 PM game. All cuts, moves, and fills are noted. Your colors are correct: red means cut, blue means airing.", "static/audio/module-3/local-swaps/module3_localswaps_12.mp3"),
    ("And that's how you swap locals! During the game, if things are running smoothly and commercials are airing as planned, start preparing a backup plan in case the game does go over.", "static/audio/module-3/local-swaps/module3_localswaps_13.mp3"),
]

# Generate Local Swaps TTS
for text, output_path in local_swaps_lines:
    synthesis_input = texttospeech.SynthesisInput(text=text)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to {output_path}") 