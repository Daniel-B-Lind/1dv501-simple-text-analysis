"""

1DV501 Final Project - HyTextAnalysis
hy_tracked_textfiles.py

Author: Daniel Lind

Defines the two classes which will be used to track text files,
and store analysis data.

"""

# Imports
import os

class HyTextFile:
    """
    This class represents the attributes of a text file undergoing
    analysis. It holds analysis results, filepath, et cetera.
    """
    
    def __init__(self, filepath):
        if(not os.path.exists(filepath)):
            raise FileNotFoundError
        if(not filepath.lower().endswith('.txt')):
            # TODO: This is fragile. What's stopping a silly guy from renaming a generic data file to .txt?
            raise ValueError("File does not appear to be a text file.")
        self.path = filepath
        self.shortname = os.path.basename(self.path)

    def append_basic_statistics(self, stats: tuple):
        """
        Stores basic statistics in HyTextFile instance.

        Arguments:
            stats: tuple containing:
                total number of lines
                total number of words
                total number of characters (no spaces)
                total number of spaces
                average words per line
                average chars per word
        
        Returns:
            None
        """

        # Sanity check - does our tuple have 6 elements as expected?
        if(len(stats) != 6):
            raise ValueError("Malformed basic statistics tuple received - does not contain 6 elements")
        
        # Unpack tuple
        (
            self.number_of_lines, 
            self.number_of_words, 
            self.number_of_characters, 
            self.number_of_spaces, 
            self.average_words_per_line,
            self.average_characters_per_word
        ) = stats
        
        self.number_of_characters_and_spaces = self.number_of_characters + self.number_of_spaces


class HyFileInventory:
    """
    Class to hold HyTextFile objects.
    Our quintessential tracker for files.
    """

    def __init__(self):
        # Initialize as empty
        self.files = []

    def add_file(self, filepath) -> HyTextFile:
        # Instantiate a HyTextFile, which requires the filepath argument,
        # then add it to the list.
        entry = HyTextFile(filepath)
        self.files.append(entry)
        return entry