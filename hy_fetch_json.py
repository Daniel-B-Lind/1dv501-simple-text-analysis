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

        # If value is a number, format it
        if isinstance(value, int):
            value = format_number(value)

        result += (f"{readable_key}: {value}\n")
    
    return result.strip()

def format_number(number: int) -> str:
    """
    Converts an integer to a human-readable string with commas separating
    thousands, millions, etc.
    
    Arguments:
        number: integer to format.
    
    Returns:
        Formatted number as a string.
    """
    return f"{number:,}"


def serialize_basic_statistics(file: hy.HyTextFile) -> str:
    """
    Fetches the basic statistics of a HyTextFile.

    Arguments:
        file: HyTextFile object to serialize the statistics of
    
    Returns:
        JSON formatted basic statistics
    """
    
    # Dictionary to hold the final results
    result = {
        'number_of_lines': file.number_of_lines,
        'number_of_words': file.number_of_words,
        'number_of_unique_words': len(file.get_unique_words()),
        'number_of_characters': file.number_of_characters,
        'number_of_characters_and_spaces': file.number_of_characters_and_spaces,
        'average_words_per_line': file.get_average_words_per_line(),
        'average_characters_per_word': file.get_average_characters_per_word()
    }

    # Return a JSON dump of the dictionary, effectively serializing it.
    return json.dumps(result)

def serialize_word_frequency_statistics(file: hy.HyTextFile) -> str:
    """
    Fetches the stored word frequency statistics of a HyTextFile.

    Arguments:
        file: HyTextFile object to serialize the statistics of.

    Returns:
        JSON formatted string of statistics
    """

    # Dictionary
    result = {
        
    }