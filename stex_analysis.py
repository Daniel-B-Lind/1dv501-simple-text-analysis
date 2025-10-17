"""

1DV501 Final Project - SimpleTextAnalysis
stex_analysis.py

Author: Daniel Lind

This file defines the functions which perform the text analysis itself.

Function Prefix Legend:
    invoke_* : Performs text analysis, returns values intended to map to TextFile

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
import stex_json as deserializer
import string
import math
import re
from pathlib import Path
from json import JSONDecodeError

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
                    word_count[clean_word] = word_count.get(clean_word, 0) + 1
                    
                    length = len(clean_word)
                    word_lengths[length] = word_lengths.get(length, 0) + 1
    
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
    STOP_CHARS = frozenset('!?.‽')
    
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
                
                # Here, our standard procedure diverges greatly.
                for character in word:
                    if character in STOP_CHARS and len(working_sentence) > 0:
                        # Commit working sentence to final variables.
                        finished_sentence_length = len(working_sentence)

                        # TODO: Messy conditional.. updates shortest_sentence if it was empty or if our last finished sentence is shorter.
                        # Also note that we are only considering sentence length by words, not characters.
                        # Via this logic, "Greetings, fellow!" is just as long as "Hi Jim."
                        if finished_sentence_length < len(shortest_sentence) or len(shortest_sentence) == 0:
                            shortest_sentence = working_sentence.copy()
                        if finished_sentence_length > len(longest_sentence):
                            longest_sentence = working_sentence.copy()
                        
                        # Update sentence distribution dictionary
                        sentence_distribution[finished_sentence_length] = sentence_distribution.get(finished_sentence_length, 0) + 1
                        
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

    letter_count = 0        # .isalpha()
    digit_count = 0         # .isdigit()
    punctuation_count = 0   # in string.punctuation
    space_count = 0         # .isspace()
    other_count = 0         # catch-all

    with open(file.path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            for character in line:
                if character in string.ascii_letters:
                    letter_count += 1
                elif character.isspace():
                    space_count += 1
                elif character.isdigit():
                    digit_count += 1
                elif character in string.punctuation:
                    punctuation_count += 1
                else:
                    other_count += 1

                # Add to occurrences dictionary.
                character_occurrences[character] = character_occurrences.get(character, 0) + 1
    
    # Sort dictionary by values.
    sorted_character_occurrences = dict(sorted(character_occurrences.items(), key=lambda item: item[1], reverse=True))

    return (
        sorted_character_occurrences,
        letter_count,
        digit_count,
        punctuation_count,
        space_count,
        other_count
    )
    
def invoke_trigram_analysis(file: stex.TextFile, maximum_words: int = 65536) -> dict[str, int]:
    """
    Performs trigram analysis on the given TextFile, looking at the beginnings
    and ends of words to obtain word boundary trigrams.
    
    Arguments:
        file: TextFile to consider
        maximum_words: int, the amount of words to process. diminishing returns after a while.
        
    Returns:
        Tuple containing:
            Dictionary containing trigram occurrences, which can be compared to
            samples of known languages.
    """
    
    word_boundary_trigrams_occurrences = {}
    
    # Keep track of the amount of words we've processed so we break if we exceed maximum_length
    processed_words = 0
    
    with open(file.path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            # Strip everything which isn't lowercase ascii (or space)
            # from the line before proceeding.
            cleaned_line = "".join(ch.lower() if ch.isalpha() or ch.isspace() else "" for ch in line)
            
            if processed_words > maximum_words:
                # We've reached our limit, abort.
                break
            
            # Proceed as planned
            for word in cleaned_line.split():
                processed_words += 1
                
                # Is the word too small to be meaningfully split into trigrams?
                if len(word) <= 3:
                    # Treat the entire word as a trigram.
                    # Trust me on this.
                    word_boundary_trigrams_occurrences[word] = word_boundary_trigrams_occurrences.get(word, 0) + 1
                    continue
                
                # Take both the beginning and ending of the word and append them.
                # Yes, a word like 'else' will be appended both as '$els' and '$lse',
                # but this will work for our analysis.
                beginning_trigram = f'${word[0:3]}'
                ending_trigram = f'{word[-3:]}$'
                
                # Check if the key exists in the dictionary and increment it. Otherwise, add it.
                word_boundary_trigrams_occurrences[beginning_trigram] = word_boundary_trigrams_occurrences.get(beginning_trigram, 0) + 1
                word_boundary_trigrams_occurrences[ending_trigram] = word_boundary_trigrams_occurrences.get(ending_trigram, 0) + 1
    
    sorted_dict = dict(sorted(word_boundary_trigrams_occurrences.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_dict

def invoke_find_closest_trigram_sample(trigrams: dict) -> dict[str, float]:
    """
    Iterates through all language sample Json files available
    and attempts to find a closest match in terms of trigram distribution
    to the provided sample dictionary.
    
    This is extensible by adding more language sample files under resources/
    with the naming convention "lang_sample_[x].json" where [x] is the language
    name and the file is generated by the auxiliary trigram_sample_generator.py script.
    
    Arguments:
        trigrams: dict[str, int] containing keys: trigrams and values: occurrences
    
    Returns:
        Dictionary with key: language name, value: percentage confidence in float
    """
    # Start by normalizing our unknown trigram dictionary.
    # This is what we'll compare all candidates to.
    normalized_trigrams = _normalize_dictionary(trigrams)
    
    # We're about to read some pretty large JSON blobs into memory.
    # First, get a list of paths to the lang_sample_x.json files.
    resources_directory = Path("resources")
    # Gets a list of all lang_sample files.
    paths = list(resources_directory.rglob("lang_sample_*.json"))
    
    # This will hold our final mappings.
    results = {}
    
    for lang_sample_path in paths:
        try:
            candidate_trigram_sample = deserializer.deserialize_from_file(lang_sample_path)
        except FileNotFoundError:
            # what the fuck? TODO: ehh????
            raise FileNotFoundError("Despite appearing in a wildcard, a file was not found. This confuses me.")
        except JSONDecodeError:
            # File was not valid json, ignore it!
            continue
        
        # candidate_trigram_sample contains mappings of word boundary trigram frequencies
        # for a known language. The dictionary may look something like this.
        # '$ste': 3, 'tep$': 3
        # We want to convert these mappings to percentages in regards to the total
        # amount of trigrams in the file.
        normalized_candidate = _normalize_dictionary(candidate_trigram_sample)
        
        # TODO: oof.
        language_name = lang_sample_path.stem.replace("lang_sample_", "")
        
        # Use cosine similarity to map the similarity of the candidate
        # to the unknown dictionary. The more equal trigram distribution, 
        # the higher likelihood of the languages being the same.
        similarity = _cosine_similarity(normalized_trigrams, normalized_candidate)
        results[language_name] = similarity

    # As is customary, sort before returning to avoid restorting later.
    sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
    
    return sorted_results

# helper functions
def _normalize_dictionary(dictionary: dict) -> dict:
    """
    Given a dictionary of type [x, int], this will
    attempt to normalize it by converting total occurrences of
    x into percentages of total values.
    """
    total_values = sum(dictionary.values())
    normalized_dict = {}
    for key, count in dictionary.items():
        normalized_value = count / total_values
        normalized_dict[key] = normalized_value
    return normalized_dict        
    
def _cosine_similarity(a: dict, b: dict) -> float:
    """
    Given two dictionaries, this function will perform
    cosine similarity analysis to find how similar they are.
    https://www.geeksforgeeks.org/dbms/cosine-similarity/
    
    Returns:
        float of distribution similarity
    """
    keys = set(a.keys()) | set(b.keys())
    dot = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    norm_a = math.sqrt(sum(v*v for v in a.values()))
    norm_b = math.sqrt(sum(v*v for v in b.values()))
    return dot / (norm_a * norm_b)