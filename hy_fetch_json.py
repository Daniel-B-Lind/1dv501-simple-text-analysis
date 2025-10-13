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

def fetch_basic_statistics(files: hy.HyTextFile):
    """
    Fetches the basic statistics of one or multiple HyTextFiles.

    Arguments:
        files: list of files to consider. can be a single file or several.
    
    Returns:
        JSON formatted basic statistics
    """
    # Here, we have to pull a somewhat gross trick.
    # 'files' can either be a single file, or if the user is simultaneously checking multiple text files,
    # it can also be a list. We're gonna work under the assumption that it *is* a list further on for generalization,
    # which means we'll have to normalize it to a list containing a single element if it isn't already a list.
    if not isinstance(files, list):
        files = [files]

    # Dictionary to hold the final results
    result = {}

    # List of attributes that should be *summed*
    sum_attributes = [
        'number_of_lines',
        'number_of_words',
        'number_of_characters', 
        'number_of_characters_and_spaces'
    ]

    # Full disclosure: I did consult an LLM for some pointers on what the best way to go about this would be.
    # We're using dictionary comprehension along with getattr (https://www.w3schools.com/python/ref_func_getattr.asp)
    # in order to dynamically access the attributes and insert them into the dictionary.
    for attr in sum_attributes:
        # We use getattr() to dynamically access the attribute on each file object
        result[f'total_{attr}'] = sum(getattr(file, attr) for file in files)
    
    # Even though each HyTextFile object already has its own average calculated,
    # since we might now be accounting for multi-HyTextFile averages rather than single files,
    # let's re-calculate an average over the 'total' sums we have in result as of right now.
    # Don't fret - the individual averages will still be useful when doing comparisons!
    total_words = result['total_number_of_words']
    total_lines = result['total_number_of_lines']
    total_chars_no_space = result['total_number_of_characters']

    result['total_average_words_per_line'] = (
        total_words / total_lines
        if total_lines else 0 
    )
    result['total_average_characters_per_word'] = (
        total_chars_no_space / total_words
        if total_words else 0
    )

    # Return a JSON dump of the dictionary, effectively serializing it.
    return json.dumps(result)