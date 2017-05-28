'''
NWVideoExtract
v1.0 - alpha
Kurt Höblinger aka NitricWare
MIT License

This python script requires ffmpeg and is currently
in an alpha state. Therefore it has some serious
flaws. It won't check wheter the input is what it
expects or not. This could lead to data loss.

Feel free to add your enhancments and send me a
pull request!
'''

import subprocess
import datetime
import os
import json

working_dir = ""
timecode_json = ""
all_segments = []

print("NWVideoExtractor v1.0")
while True:
    video_path = input("Please enter the video path: ")
    if os.path.exists(video_path):
        working_dir = os.path.dirname(video_path)
        timecode_json = os.path.join(working_dir,
                                     os.path.splitext(video_path)[0]+".json")
        break
    print("Invalid path. Try again.")

while True:
    print("Would you like to add timecodes or use an existing file?")
    uin = input("[A]dd timecodes or [U]se existing file: ")
    if uin.upper() == "A":
        print("You chose to add timecodes.")
        print("A new file will be created for this.")
        add = True
        while True:
            title = input("Title: ")
            start = input("Start Timecode: ")
            end = input("End Timecode: ")
            print("Calculating duration...")
            # Calculating duration
            # Splitting up hh:mm:ss formatted input
            start_tup = start.split(':')
            end_tup = end.split(':')
            # Creating two datetime object with collected data
            start_sec = datetime.datetime(year=1990,
                                          month=2,
                                          day=19,
                                          hour=int(start_tup[0]),
                                          minute=int(start_tup[1]),
                                          second=int(start_tup[2]))
            end_sec = datetime.datetime(year=1990,
                                        month=2,
                                        day=19,
                                        hour=int(end_tup[0]),
                                        minute=int(end_tup[1]),
                                        second=int(end_tup[2]))
            # Calculating the difference
            diff = end_sec - start_sec
            # Creating a new tuple, containing the title, the start hh:mm:ss and the end
            segment = [title, start, str(diff)]
            # Appending segment to tuple containing all segments
            all_segments.append(segment)
            uin = input("[C]ontinue or [M]ove on? ")
            if uin.upper() != "C":
                print("Creating JSON file...")
                with open(timecode_json, 'w') as jsonfile:
                    json.dump(all_segments, jsonfile)
                print("JSON file created.")
                break
        break
    elif uin.upper() == "U":
        if os.path.exists(timecode_json):
            print("Reading JSON file...")
            with open(timecode_json, 'r') as jsonfile:
                all_segments = json.load(jsonfile)
            print("JSON file read.")
            break
        print("No JSON file found. Create a new one.")

print("Ready to split video file?")
uin = input("[Y]es or [E]xit? ")

if uin.upper() == "Y":
    # Add control mechanismns here
    for segment in all_segments:
        output_file = os.path.join(working_dir, segment[0]+".mp4")
        ffmpeg_command = "ffmpeg -i %s -ss %s -t %s -c copy %s" % (video_path,
                                                                   segment[1],
                                                                   segment[2],
                                                                   output_file)
        print(ffmpeg_command)
        subprocess.run(ffmpeg_command, shell=True)
