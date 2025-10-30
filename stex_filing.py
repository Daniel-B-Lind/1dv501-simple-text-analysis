"""

1DV501 Final Project - SimpleTextAnalysis
stex_filing.py

Author: Daniel Lind

Defines the class which will be used to track text files,
and store analysis data.

Function Prefix Legend:
    append_* : Store data in TextFile object
    get_* : Return some value based on data in TextFile object

"""

# Imports
import os
import numpy as np

class TextFile:
    """
    This class represents the attributes of a text file undergoing
    analysis. It holds analysis results, filepath, et cetera.,
    while also containing methods to get additional statistics
    from saved results.
    """
    
    def __init__(self, filepath: str) -> None:
        # Before creating an instance of this object, do some basic sanity checks.
        if(not os.path.exists(filepath)):
            raise FileNotFoundError
        if(not filepath.lower().endswith('.txt')):
            raise ValueError("Extension mismatch. Please provide a text file.")
        
        # Just because a file ends with .txt doesn't mean it's valid text.
        # To test it further, we'll open the file as UTF-8 and read the first
        # few characters. 
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # This is technically kind of janky, but in any case,
                # if the final contains binary data in the first 512
                # characters, we'll flag it as invalid.
                #
                # This is also not foolproof. The first 512 bytes could
                # be perfectly valid while the rest is a corrupted mess.
                # Short of reading through the entire file ahead of time,
                # there's not a lot to do about that, so we'll have to
                # rely on it being caught later.
                f.read(512) 
        except UnicodeDecodeError:
            raise ValueError("File is not valid UTF-8 text. Please provide a valid text file.")
        
        self.path = filepath
        self.shortname = os.path.basename(self.path)

    # ----------- DATA SAVING FUNCTIONS  -----------
    def append_basic_statistics(self, stats: tuple) -> None:
        """
        Stores basic statistics in HyTextFile instance.

        Arguments:
            stats: tuple containing:
                total number of lines
                total number of words
                total number of characters (no spaces)
                total number of spaces
        
        Returns:
            None
        """

        # Sanity check - does our tuple have 4 elements as expected? TODO: is this even remotely sane
        if(len(stats) != 4):
            raise ValueError("Malformed basic statistics tuple received - does not contain 4 elements")
        
        # Unpack tuple
        (
            self.number_of_lines, 
            self.number_of_words, 
            self.number_of_characters, 
            self.number_of_spaces, 
        ) = stats
        
        self.number_of_characters_and_spaces = self.number_of_characters + self.number_of_spaces
    
    def append_word_frequency_statistics(self, stats: tuple) -> None:
        """
        Stores the results of a corresponding Word Frequency Analysis in HyTextFile instance.

        Arguments:
            stats: tuple containing:
                dictionary containing:
                    word occurrences (key: word(str), value: occurrences(int))
                dictionary containing
                    word length occurrences (key: length(int), value: occurrences(int))
        """
        (
            self.word_occurrences,
            self.word_length_occurrences
        ) = stats
        
    def append_sentence_statistics(self, stats: tuple[str, str, dict[int, int]]) -> None:
        """
                    
        """
        (
            self.shortest_sentence_text,
            self.longest_sentence_text,
            self.sentence_length_distribution
        ) = stats

        self.total_sentences = sum(self.sentence_length_distribution.values())

    def append_character_statistics(self, stats: tuple[dict[str, int], int, int, int, int, int]) -> None:
        """
        Stores the results of a corresponding Character Analysis.

        Arguments:
            stats: tuple containing:
                dictionary containing:
                    character occurrences (key: character(str), value: occurrences(int))
                amount of letters (int)
                amount of digits (int)
                amount of punctuation (int)
                amount of spaces (int)
                amount of other characters (int)
        """
        (
            self.character_occurrences,
            self.letter_count,
            self.digit_count,
            self.punctuation_count,
            self.space_count,
            self.other_count
        ) = stats

        self.total_characters = sum(self.character_occurrences.values())
        
    def append_language_probabilities(self, stats: dict[str, float]) -> None:
        """
        Stores the results of a trigram-based language probability analysis.
        
        Arguments:
            stats: sorted dictionary with key: language(str), value: probability(float)
        """
        self.language_probabilities = stats
        self.most_likely_language = max(stats, key=stats.get)

    # ----------- DATA RETRIEVAL FUNCTIONS -----------
    def get_average_words_per_line(self, round_to: int = 3) -> float:
        """
        Returns the average words per line, rounded to round_to decimals.
        """
        words = self.number_of_words
        lines = self.number_of_lines
        average = (words / lines) if (lines != 0) else 0        
        rounded = round(average, round_to)
        return rounded

    def get_count_of_lowercase_and_capitalized_ascii(self) -> tuple[float, float]:
        """
        Returns a tuple of how many uppercase contra lowercase ASCII characters
        appeared. Only supports standard English or Swedish alphabets..
        """

        lower_total = 0
        upper_total = 0
        
        ASCII_LOWER = set('abcdefghijklmnopqrstuvwxyzåäö')
        ASCII_UPPER = set('ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ')
    
        for character, count in self.character_occurrences.items():
            if character.islower() and character in ASCII_LOWER:
                lower_total += count
            elif character.isupper() and character in ASCII_UPPER:
                upper_total += count
    
        return lower_total, upper_total

    def get_average_characters_per_word(self, round_to: int = 3) -> float:
        """
        Returns the average characters per word, rounded to round_to decimals.
        """
        characters = self.number_of_characters
        words = self.number_of_words
        average = (characters / words) if (words != 0) else 0
        rounded = round(average, round_to)
        return rounded

    def get_average_words_per_sentence(self, round_to: int = 3) -> float:
        """ 
        Returns the average number of words per sentence, rounded to round_to decimals.
        """
        if not self.sentence_length_distribution:
            # No sentences? Weird.
            return 0

        total_words = sum(length * count for length, count in self.sentence_length_distribution.items())
        total_sentences = self.total_sentences

        average = total_words / total_sentences
        return round(average, round_to)
    
    def get_orphan_words(self) -> tuple[str]:
        """
        Finds words which only occurred a single time.

        Returns:
            Tuple of every unique word which only has a single occurrence in this HyTextFile
        """
        # Find amount of unique words (words with a count of only 1)
        orphan_words = []
        for word, count in self.word_occurrences.items():
            if count == 1:
                orphan_words.append(word)
        
        return tuple(orphan_words)

    def get_unique_words(self) -> tuple[str]:
        """
        Returns a tuple of every word which appears in the HyTextFile, with no duplicates,
        ordered by amount of appearances.
        """
        unique_words = []
        for word in self.word_occurrences.keys():
            unique_words.append(word)
        
        return tuple(unique_words)

    
    def get_top_elements_of_dictionary(self, dictionary: dict, top_n: int, constraint: set | None = None) -> dict:
        """
        Finds the N first entries in a dictionary. If the dictionary
        is sorted, which it should be, this will be the top values of it.
        May return a lower amount if the requested number of values
        exceeds the size of the dictionary.

        Args:
            dictionary: dict to consider
            top_n: amount of values to return

        Returns:
            Dictionary containing N of its topmost values
        """
        # Is top_n too big? If so, downsize it...
        if(top_n > len(dictionary)):
            top_n = len(dictionary)

        # If we have a constraint, remove the keys of a dictionary which do not match
        # the constraint (we're filtering to the set - for each key, check if it's an element of the set)
        if(constraint != None):
            filtered_dictionary = {}
            element_count = 0
            
            for key, value in dictionary.items():
                if key in constraint:
                    # If the key matches our contraint, append to filterd dictionary.
                    filtered_dictionary[key] = value
                    
                    # Optimization - since we know how many elements we've added,
                    # we can break as soon as we have enough and avoid filtering more
                    # than we need to.
                    element_count += 1
                    if (element_count >= top_n):
                        break

            # dictionary is filtered and has been sliced to top_n values
            return filtered_dictionary
        else:
            top_values = dict(list(dictionary.items())[:top_n])
            return top_values

    def get_word_length_statistics(self) -> tuple[int, int, float]:
        """
        Get some basic statistics about word length.

        Arguments:
            None
        
        Returns:
            Tuple containing:
                Length of shortest word (int)
                Length of longest word (int)
                Average word length (float)
        """
        
        # keys: lengths, values: occurrences
        word_length_dictionary = self.word_length_occurrences
        # This is also already expected to be sorted (by occurrences; we've shot ourselves in the foot..)

        # Since we only care about the keys, let's get a list of keys and sort it.
        word_lengths = list(word_length_dictionary.keys())
        sorted_word_lengths = sorted(word_lengths)

        # Now, let's get the weighted average.
        occurrences = list(word_length_dictionary.values())

        # https://stackoverflow.com/questions/72700130/calculating-weighted-average-using-two-different-list-of-lists
        average = float(np.average(word_lengths, weights=occurrences))
        
        return (
            int(sorted_word_lengths[0]),
            int(sorted_word_lengths[-1]),
            average
        )
