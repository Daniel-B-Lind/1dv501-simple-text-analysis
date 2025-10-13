import os

#You bet we're doing object oriented programming!
#There's nothing in the assignment that argues against it!


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

    def append_basic_statistics(stats: tuple):
        """
        
        """

class HyFileInventory:
    """
    Class to hold HyTextFile objects.
    Our quintessential tracker for files.
    """

    def __init__(self):
        # Initialize as empty
        self.files = []

    def add_file(self, filepath):
        # Instantiate a HyTextFile, which requires the filepath argument,
        # then add it to the list.
        entry = HyTextFile(filepath)
        self.files.append(entry)
        return entry