"""

1DV501 Final Project - HyTextAnalysis
hy_analysis.py

Author: Daniel Lind

This file defines the functions which perform the text analysis itself.

Addendum - 
    You will notice that I iterate through the file line-by-line several times,
    in different "passes." This is because I reasoned that the performance cost
    of iterating through every line several times was worth it for the readability
    and modularity of the functions in this file.

    It would, technically, be more performant to do this all in a single pass
    through the file. But for the datasets we're dealing with, which are in 
    all likelihood <50MB, I reasoned that code quality mattered more.

"""

# Imports
import hy_tracked_textfiles as hy
import re

def fetch_basic_statistics(file: hy.HyTextFile) -> tuple:
    """
    Calculates basic statistics given a file object.

    Arguments:
        file: HyTextFile entry of a tracked file
    
    Returns:
        A tuple containing, in order:
        • Total number of lines
        • Total number of words
        • Total number of characters (without spaces)
        • Total number of characters which are spaces
    """

    path = file.path

    file_number_of_lines = 0
    file_number_of_words = 0
    file_number_of_characters = 0
    file_number_of_spaces = 0

    # Read file line by line (*not* all at once in memory :D)
    # Note: errors='replace' will replace faulty unicode characters with a fallback character.
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            try:
                # Remove trailing newline but keep internal spaces
                line = line.rstrip('\n')

                file_number_of_lines += 1

                # Split into words (whitespace delimiter)
                words = line.split()
                line_number_of_words = len(words)

                # Count spaces. I'm also going to count each
                # line itself as a space (LF) to better approximate actual
                # character counts. CRLF need not apply - do not use Windows.
                file_number_of_spaces += (line.count(' ') + 1)

                # Count characters in all words (excluding spaces)
                line_number_of_characters = sum(len(word) for word in words)

                # Apply local variables for this line to the file scope
                file_number_of_words += line_number_of_words
                file_number_of_characters += line_number_of_characters
            except Exception as e:
                # Very unlikely for an exception to occur here.
                # If one does, it's probably safer to just pass it up the chain than to continue iterating.
                raise e

    # Compute averages
    average_words_per_line = file_number_of_words / file_number_of_lines if file_number_of_lines != 0 else 0
    average_characters_per_word = file_number_of_characters / file_number_of_words if file_number_of_words != 0 else 0

    # Return final ordered tuple
    return (
        file_number_of_lines,
        file_number_of_words,
        file_number_of_characters,
        file_number_of_spaces
    )

def fetch_word_frequency_statistics(file: hy.HyTextFile) -> tuple:
    """    
    Arguments:
        file: HyTextFile object
    
    Returns:
        Tuple of the following:
            - dictionary of word occurrences (key: word(str), value: occurrences(int))
            - dictionary of word lengths (key: length(int), value: occurrences(int))
    """

    path = file.path

    # Since we're analyzing words, let's normalize each word.
    # We'll convert everything to lowercase, but beyond that,
    # we only care about characters which actually make up words.
    # 
    # This can be expanded on to support other languages, or be
    # adjusted more granularly depending on what characters one
    # considers "part of a word."
    VALID_CHARS = "abcdefghijklmnopqrstuvwxyzåäö'-"

    # Since we are dealing with 'big data', the simple solution
    # to consider substrings or rebuild each word based by comparing
    # against VALID_CHARS would be horribly slow. For this reason,
    # we'll use a compiled Regex.
    pattern = re.compile(f"[^{VALID_CHARS}]+") 

    # Key: word in lowercase
    # Value: number of occurrences
    word_count = {}

    # Key: word length
    # Value: number of occurrences
    word_lengths = {}

    # Iterate through text file and populate dictionaries.
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            words = line.split()
            for word in words:
                # Normalize by uncapitalizing and subsequently regexing
                word = word.lower()
                clean_word = pattern.sub('', word)
                if clean_word:
                    # Append to both dictionaries
                    if clean_word in word_count:
                        word_count[clean_word] += 1
                    else:
                        word_count[clean_word] = 1
                    
                    length = len(clean_word)
                    if length in word_lengths:
                        word_lengths[length] += 1
                    else:
                        word_lengths[length] = 1
    
    # Dictionaries are fully populated.
    # Sort them by values (https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value)
    sorted_word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))
    sorted_word_lengths = dict(sorted(word_lengths.items(), key=lambda item: item[1], reverse=True))

    return (
        sorted_word_count,
        sorted_word_lengths,
    )
