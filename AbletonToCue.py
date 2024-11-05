# Convert .als to .cue file format:
# Usage example:
# python3 AbletonToCue.py "/path/to/yourfile.als"

import gzip
import xml.etree.ElementTree as ET
import sys
import os

def convert_als_to_xml(als_path):
    """
    Convert a compressed .als (Ableton Live Set) file to XML format by decompressing it.
    
    Parameters:
        als_path (str): Path to the .als file to be converted.
    
    Returns:
        str: Path to the converted .xml file.
    """
    xml_path = als_path.replace(".als", ".xml")
    with gzip.open(als_path, 'rb') as f_in:
        with open(xml_path, 'wb') as f_out:
            f_out.write(f_in.read())
    return xml_path

def parse_start_time(seconds):
    """
    Format a timestamp (in seconds) to cue file time format (HH:MM:SS).
    
    Parameters:
        seconds (float): Timestamp in seconds.
    
    Returns:
        str: Formatted timestamp as HH:MM:SS.
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def process_als_file(als_path):
    """
    Process an Ableton Live Set (.als) file and output its track information in .cue format.
    
    Parameters:
        als_path (str): Path to the .als file to be processed.
    """
    # Convert .als file to XML for parsing
    xml_path = convert_als_to_xml(als_path)
    
    # Parse the XML structure
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Write .cue header information
    print('TITLE "my cool cue file"')
    print('PERFORMER "Unknown Artist"')
    print(f'FILE "{als_path}"')

    track_number = 1  # Initialize track number

    # Iterate through each audio track in the Ableton project
    for track in root.findall(".//AudioTrack"):
        track_name = track.find(".//Name/UserName").get("Value", "")
        clip = track.find(".//AudioClip")

        if clip is not None:
            # Extract clip information
            clip_name = clip.find("Name").get("Value", "")
            start_time = float(clip.get("Time", 0))
            duration = float(clip.find("CurrentEnd").get("Value", 0)) - start_time
            file_path = clip.find(".//SampleRef/FileRef/Path").get("Value", "")
            start_time_formatted = parse_start_time(start_time)

            # Write .cue track information
            print(f'TRACK {track_number:02} AUDIO')
            print(f'TITLE "{clip_name}"')
            print(f'PERFORMER "Unknown Artist"')
            print(f'FILE "{file_path}" WAVE')
            print(f'INDEX 01 {start_time_formatted}')
            
            track_number += 1

    # Clean up temporary XML file
    os.remove(xml_path)

if __name__ == "__main__":
    # Check if correct arguments are provided
    if len(sys.argv) != 2:
        print("Usage: python AbletonToCue.py <path_to_als_file>")
        sys.exit(1)

    als_path = sys.argv[1]
    
    # Verify that input is an .als file
    if not als_path.endswith(".als"):
        print("The input file must be a .als file.")
        sys.exit(1)

    # Process the .als file and convert to .cue format
    process_als_file(als_path)
