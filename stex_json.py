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

def serialize_all(file: stex.TextFile) -> str:
    """
    Serializes all elements of a TextFile (Basic, Words, Sentences, Characters)
    and returns the full json containing all data.
    
    Arguments:
        file: TextFile to consider
    
    Returns:
        Export-ready JSON string.
    """
    result = {
        'basic_analysis': serialize_basic_statistics(file),
        'word_analysis': serialize_word_frequency_statistics(file),
        'sentence_analysis': serialize_sentence_statistics(file),
        'character_analysis': serialize_character_statistics(file)
    }
    
    return json.dumps(result, indent=4)

def serialize_basic_statistics(file: stex.TextFile) -> dict:
    """
    Fetches the basic statistics of a HyTextFile.

    Arguments:
        file: TextFile object to serialize the statistics of
    
    Returns:
        JSON formatted basic statistics
    """
    
    # Dictionary to hold the final results
    result = {
        'line_count': file.number_of_lines,
        'word_count': file.number_of_words,
        'unique_words': len(file.get_unique_words()),
        'character_count_basic': file.number_of_characters,
        'character_count_with_spaces_basic': file.number_of_characters_and_spaces,
        'average_words_per_line': file.get_average_words_per_line(),
        'average_characters_per_word': file.get_average_characters_per_word()
    }

    # Return a JSON dump of the dictionary, effectively serializing it.
    return result

def serialize_word_frequency_statistics(file: stex.TextFile) -> dict:
    """
    Fetches the stored word frequency statistics of a HyTextFile.

    Arguments:
        file: TextFile object to serialize the statistics of.

    Returns:
        JSON formatted string of statistics
    """

    # Dictionary
    result = {
        'word_occurrences': file.word_occurrences,
        'word_length_occurrences': file.word_length_occurrences
    }
    
    return result

def serialize_sentence_statistics(file: stex.TextFile) -> dict:
    """
    
    """
    
    result = {
        'sentence_count': file.total_sentences,
        'longest_sentence':
            {
            'length': len(file.longest_sentence_text),
            'text': file.longest_sentence_text
            },
        'shortest_sentence':
            {
            'length': len(file.shortest_sentence_text),
            'text': file.shortest_sentence_text
            },
        'sentence_length_occurrences': file.sentence_length_distribution
    }
    
    return result

def serialize_character_statistics(file: stex.TextFile) -> dict:
    """
    
    """
    
    result = {
        'characters': 
            {
            'total': file.total_characters,
            'letters': file.letter_count,
            'digits': file.digit_count,
            'punctuation': file.punctuation_count,
            'spaces': file.space_count,
            'other': file.other_count
            },
        'character_occurrences': file.character_occurrences
    }
    
    return result