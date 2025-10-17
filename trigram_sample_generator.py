"""
trigram_sample_generator.py
Author: Daniel Lind

An auxiliary file used to generate standalone JSON files containing the trigram occurrences
in text files.

"""
import sys
import json
import os
from stex_analysis import invoke_trigram_analysis
from stex_filing import TextFile

def main(input_path: str, output_path: str, maximum_words_to_parse: int = 65536) -> None:
    dummy_file = TextFile(input_path)
    trigram_dictionary = invoke_trigram_analysis(dummy_file, maximum_words_to_parse)
    json_trigrams = json.dumps(trigram_dictionary, ensure_ascii=False, indent=4)
    
    save_output(json_trigrams, output_path)

def save_output(data: str, output_path: str) -> bool:
    """
    Saves the data to the output path, handles overwriting confirmation,
    and prompts for a new path on error.
    
    Returns:
        True on successful save, False otherwise.
    """
    while True:
        # Check if the file exists and prompt for overwrite
        if os.path.exists(output_path):
            response = input(f"File '{output_path}' already exists. Overwrite? (y/N) ").lower()
            if response != 'y':
                print("Output cancelled by user. Please re-run with a different path.")
                return False

        try:
            # Attempt to save the data
            with open(output_path, 'w') as f:
                f.write(data)
            print(f"Successfully saved trigrams to: {output_path}")
            return True
            
        except IOError as e:
            print(f"Error writing to {output_path}: {e}")
            new_path = input("Please enter a new output path to retry.\n> ")
        
            # Update the path and loop to retry
            output_path = new_path
        except Exception as e:
            # Catch other potential errors (e.g., permission denied)
            print(f"An unexpected error occurred: {e}")
            return False

if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python3 trigram_sample_generator.py [input_path] [output_path] <maximum words>")
        sys.exit(1)
    
    if(len(sys.argv) == 4):
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        main(sys.argv[1], sys.argv[2])
