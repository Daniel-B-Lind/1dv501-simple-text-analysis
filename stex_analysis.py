"""

1DV501 Final Project - SimpleTextAnalysis
stex_analysis.py

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
import stex_filing as stex
import re

def invoke_basic_statistics(file: stex.TextFile) -> tuple:
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
    
    file_number_of_lines = 0
    file_number_of_words = 0
    file_number_of_characters = 0
    file_number_of_spaces = 0

    # Read file line by line (*not* all at once in memory :D)
    # Note: errors='replace' will replace faulty unicode characters with a fallback character.
    with open(file.path, 'r', encoding='utf-8', errors='replace') as f:
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

    # Return final ordered tuple
    return (
        file_number_of_lines,
        file_number_of_words,
        file_number_of_characters,
        file_number_of_spaces
    )

def invoke_word_frequency_statistics(file: stex.TextFile) -> tuple[dict[str,int], dict[int,int]]:
    """    
    Arguments:
        file: HyTextFile object
    
    Returns:
        Tuple of the following:
            - dictionary of word occurrences (key: word(str), value: occurrences(int))
            - dictionary of word lengths (key: length(int), value: occurrences(int))
    """

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
    with open(file.path, 'r', encoding='utf-8', errors='replace') as f:
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
    
def invoke_sentence_statistics(file: stex.TextFile) -> tuple[str, str, dict[int, int]]:
    """
    Performs rudimentary sentence analysis on the provided text file.
    
    Arguments:
        file: TextFile object to consider.
        
    Returns:
        tuple containing:
            shortest identified sentence (str)
            longest identified sentence (str)
            dictionary of sentence length distribution (key: length(int), value: occurrences(int))
    """
    
    # So, sentence analysis doesn't play nicely with the system we've built so far.
    # Sentences can spill over across lines, so if we naïvely only check line-by-line
    # we won't get any valid data.
    #
    # My approach here will leave a lot to be desired if I'm honest, since this exact 
    # breed of "stringbuilder shenanigans" is something I have explicitly avoided up until now.
    
    # Define which characters denote the end of a sentence.
    # Using a set here for O(1) lookup time.
    # TODO: This is still a little fragile in case this punctuation is used
    # but not intended to be a full stop, e.g. abbreviations (see what I did there?)
    # This works for now but word detection could be improved.
    STOP_CHARS = frozenset(read_resource_file('stopchars'))
    
    # This stores the current sentence we're working our way through.
    working_sentence = []
    
    # These three will be our 'finals' which are returned as a tuple.
    shortest_sentence = []
    longest_sentence = []
    sentence_distribution = {}
    
    # Load file and iterate through it as before.
    with open(file.path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            for word in line.split():
                # Sentence is still ongoing. Add our word to the building list.
                working_sentence.append(word)
                
                # Here, our standard procedure does as Phoenix HyperSpace does and ✨diverges greatly✨ (that's a reference you don't get)
                for character in word:
                    if(character in STOP_CHARS and len(working_sentence) > 0):
                        # Commit working sentence to final variables.
                        finished_sentence_length = len(working_sentence)

                        # TODO: Messy conditional.. updates shortest_sentence if it was empty or if our last finished sentence is shorter.
                        # Also note that we are only considering sentence length by words, not characters.
                        # Via this logic, "Greetings, fellow!" is just as long as "Hi Jim."
                        if(finished_sentence_length < len(shortest_sentence) or len(shortest_sentence) == 0):
                            shortest_sentence = working_sentence.copy()
                        if(finished_sentence_length > len(longest_sentence)):
                            longest_sentence = working_sentence.copy()
                        
                        # Update sentence distribution dictionary
                        if finished_sentence_length in sentence_distribution:
                            sentence_distribution[finished_sentence_length] += 1
                        else:
                            sentence_distribution[finished_sentence_length] = 1
                        
                        # Reset working sentence.
                        working_sentence = []
    
    # Sort distribution directory by frequency of values.
    sorted_sentence_distribution = dict(sorted(sentence_distribution.items(), key=lambda item: item[1], reverse=True))

    return (
        " ".join(shortest_sentence),
        " ".join(longest_sentence),
        sorted_sentence_distribution
    )

def invoke_character_statistics(file: stex.TextFile) -> tuple[dict[str, int], int, int, int, int, int]:
    """
    Iterates through the provided TextFile and returns a dictionary
    containing how many times each character occurs.

    Arguments:
        file: TextFile to consider
    
    Returns:
        tuple containing:
            dictionary (key: character, value: occurrences)
            int of letter count
            int of digit count
            int of punctuation count
            int of spaces count
            int of other count
    """

    character_occurrences = {}

    LETTERS = frozenset(read_resource_file('letters'))
    DIGITS = frozenset(read_resource_file('digits'))
    PUNCTUATION = frozenset(read_resource_file('punctuation'))
    # Anything not defined in these files will be counted as 'other'.

    letter_count = 0
    digit_count = 0
    punctuation_count = 0
    space_count = 0
    other_count = 0

    with open(file.path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            for character in line:
                if character in LETTERS:
                    letter_count += 1
                elif character == ' ':
                    space_count += 1
                elif character in DIGITS:
                    digit_count += 1
                elif character in PUNCTUATION:
                    punctuation_count += 1
                else:
                    other_count += 1

                # Add to occurrences dictionary.
                if character in character_occurrences:
                    character_occurrences[character] += 1
                else:
                    character_occurrences[character] = 1
    
    return (
        character_occurrences,
        letter_count,
        digit_count,
        punctuation_count,
        space_count,
        other_count
    )

# Helper Functions
def read_resource_file(name: str) -> str:
    """
    Reads a file from the 'resources' folder, located by name,
    and returns its contents.
    
    Arguments:
        name: The *name* (not path!) of the file, located in the accompanying /resources folder.
    
    Returns:
        str
    """
    content = ''
    with open(f"resources/{name}", 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    return content.strip()