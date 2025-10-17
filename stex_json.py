"""

1DV501 Final Project - SimpleTextAnalysis
stex_json.py

Author: Daniel Lind

This file contains functions responsible for serializing data stored in TextFile objects
to JSON, which can either be saved to disk as-is or passed through a 
"friendly deserializer" also located in this file to translate into something fit
to be displaced to the user inline on Jupyter.

"""

# Imports
import json
import stex_filing as stex

def serialize_basic_statistics(file: stex.TextFile) -> str:
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

def serialize_word_frequency_statistics(file: stex.TextFile) -> str:
    """
    Fetches the stored word frequency statistics of a HyTextFile.

    Arguments:
        file: HyTextFile object to serialize the statistics of.

    Returns:
        JSON formatted string of statistics
    """
    raise NotImplementedError
    # Dictionary
    result = {
        
    }
    
    return json.dumps(result)