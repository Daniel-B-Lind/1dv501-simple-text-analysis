"""

1DV501 Final Project - HyTextAnalysis
hy_fetch_json.py

Author: Daniel Lind

This file contains functions responsible for serializing data stored in HyTextFile objects
to JSON, which can either be saved to disk as-is or passed through a 
"friendly deserializer" also located in this file to translate into something fit
to be displaced to the user inline on Jupyter.

"""

# Imports
import json
import hy_tracked_textfiles as hy

def json_to_pretty(json_str: str) -> str:
    """
    Converts a JSON serialized string to a human readable and indented
    string.

    Arguments:
        json_str: JSON string to deserialize.
    
    Returns:
        Prettied, readable, printable string.
    """
    # Deserialize JSON string
    data = json.loads(json_str)
    
    # Build pretty string
    result = ''
    for key, value in data.items():
        # Convert snake_case to Title Case
        readable_key = key.replace('_', ' ').capitalize()
        result += (f"{readable_key}: {value}\n")
    
    return result.strip()


def fetch_basic_statistics(files: hy.HyTextFile) -> str:
    """
    Fetches the basic statistics of one or multiple HyTextFiles.

    Arguments:
        files: list of files to consider. can be a single file or several.
    
    Returns:
        JSON formatted basic statistics
    """
    
    # Dictionary to hold the final results
    result = {
        'total_number_of_lines': file.number_of_lines,
        'total_number_of_words': file.number_of_words,
        'total_number_of_characters': file.number_of_characters,
        'total_number_of_characters_and_spaces': file.number_of_characters_and_spaces,
        'total_average_words_per_line': file.average_words_per_line,
        'total_average_characters_per_word': file.average_characters_per_word,
    }

    # Return a JSON dump of the dictionary, effectively serializing it.
    return json.dumps(result)