# Convert .als to .cue: 
# python3 AbletonToCue.py "/mnt/e/martinradio/musicproduction/ableton projects/inflation mix Project/inflation 2.als"

import gzip
import xml.etree.ElementTree as ET
import sys
import os

def convert_als_to_xml(als_path):
    xml_path = als_path.replace(".als", ".xml")
    with gzip.open(als_path, 'rb') as f_in:
        with open(xml_path, 'wb') as f_out:
            f_out.write(f_in.read())
    return xml_path

def parse_start_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def process_als_file(als_path):
    xml_path = convert_als_to_xml(als_path)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    print('TITLE "my cool cue file"')
    print('PERFORMER "Unknown Artist"')
    print(f'FILE "{als_path}"')

    track_number = 1

    for track in root.findall(".//AudioTrack"):
        track_name = track.find(".//Name/UserName").get("Value", "")
        clip = track.find(".//AudioClip")
        if clip is not None:
            clip_name = clip.find("Name").get("Value", "")
            start_time = float(clip.get("Time", 0))
            duration = float(clip.find("CurrentEnd").get("Value", 0)) - start_time
            file_path = clip.find(".//SampleRef/FileRef/Path").get("Value", "")
            start_time_formatted = parse_start_time(start_time)

            print(f'TRACK {track_number:02} AUDIO')
            print(f'TITLE "{clip_name}"')
            print(f'PERFORMER "Unknown Artist"')
            print(f'FILE "{file_path}" WAVE')
            print(f'INDEX 01 {start_time_formatted}')
            
            track_number += 1

    os.remove(xml_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python AbletonToCue.py <path_to_als_file>")
        sys.exit(1)

    als_path = sys.argv[1]
    if not als_path.endswith(".als"):
        print("The input file must be a .als file.")
        sys.exit(1)

    process_als_file(als_path)
