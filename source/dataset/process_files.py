import os
import re

def extract_puzzles_from_file(file_path):
    """Extract Sokoban puzzles from a single file."""
    with open(file_path, 'r') as file:
        content = file.read()

    # Split content into sections by the separator
    sections = re.split(r"::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::", content)

    # If there are at least three sections, puzzles are in the third section onward
    if len(sections) >= 3:
        puzzles_section = "".join(sections[2:])
        # Extract puzzles by identifying the "Author" and "Title" lines
        puzzles = re.split(r"\n\n", puzzles_section)
        # puzzles = re.split(r"\n(?=Author:)", puzzles_section)
        puzzles = [re.split(r"\n(?=Author:)", lll)[0] for lll in puzzles]
        
        print(puzzles)
        return puzzles

    return []

def process_folder(input_folder, output_file):
    """Process all files in a folder and save extracted puzzles to an output file."""
    all_puzzles = []

    for root, _, files in os.walk(input_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name.startswith('Magic') or file_name.startswith('Original'):
                print(f"Processing file: {file_path}")
                puzzles = extract_puzzles_from_file(file_path)

                all_puzzles.extend(puzzles)

    # Save all puzzles into the output file
    with open(output_file, 'w') as out_file:
        for index, puzzle in enumerate(all_puzzles):
            if len(puzzle.strip()) > 5:
                out_file.write("%%ID:" + str(index) + "%%\n" + puzzle + "\n\n")

    print(f"Finished processing. Puzzles saved to {output_file}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python sokoban_parser.py <input_folder> <output_file>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_file = sys.argv[2]

    process_folder(input_folder, output_file)