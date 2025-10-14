"""

1DV501 Final Project - SimpleTextAnalysis
stex_filing.py

Author: Daniel Lind

Defines the two classes which will be used to track text files,
and store analysis data.

"""

# Imports
import os
import numpy as np

class TextFile:
    """
    This class represents the attributes of a text file undergoing
    analysis. It holds analysis results, filepath, et cetera.
    """
    
    def __init__(self, filepath: str) -> None:
        if(not os.path.exists(filepath)):
            raise FileNotFoundError
        if(not filepath.lower().endswith('.txt')):
            # TODO: This is fragile. What's stopping a silly guy from renaming a generic data file to .txt?
            raise ValueError("File does not appear to be a text file.")
        self.path = filepath
        self.shortname = os.path.basename(self.path)

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

    def get_average_words_per_line(self, round_to: int = 3) -> float:
        """
        Returns the average words per line, rounded to round_to decimals.
        """
        words = self.number_of_words
        lines = self.number_of_lines
        average = words / lines
        rounded = round(average, round_to)
        return rounded

    def get_average_characters_per_word(self, round_to: int = 3) -> float:
        """
        Returns the average characters per word, rounded to round_to decimals.
        """
        characters = self.number_of_characters
        words = self.number_of_words
        average = characters / words
        rounded = round(average, round_to)
        return rounded

    
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

    
    def get_top_words(self, top_n: int) -> dict:
        """
        Finds the N most common words.
        May return a lower amount if the requested number of values
        exceeds the size of the dictionary.

        Returns:
            Dictionary containing N of the most common words.
        """
        words = self.word_occurrences

        # Is top_n too big? If so, downsize it...
        if(top_n > len(words)):
            top_n = len(words)

        # Dictionary is already sorted, so we simply taken N off the top
        most_common_words = dict(list(words.items())[:top_n])
        return most_common_words

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


class FileInventory:
    """
    Class to hold HyTextFile objects.
    Our quintessential tracker for files.
    """

    def __init__(self):
        # Initialize as empty
        self.files = []

    def add_file(self, filepath) -> TextFile:
        # Instantiate a HyTextFile, which requires the filepath argument,
        # then add it to the list.
        entry = TextFile(filepath)
        self.files.append(entry)
        return entry