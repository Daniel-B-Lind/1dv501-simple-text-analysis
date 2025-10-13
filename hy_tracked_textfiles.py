import os

"""
    You bet we're doing object oriented programming!
    There's nothing in the assignment that argues against it!

    This class represents the attributes of a text file undergoing
    analysis. It holds analysis results, filepath, et cetera.
"""
class HyTextFile:
    def __init__(self, filepath):
        if(not os.path.exists(filepath)):
            raise FileNotFoundError
        self.path = filepath

"""
    Class to hold HyTextFile objects.
    Our quintessential tracker for files.
"""
class HyFileInventory:
     def __init__(self):
        # Initialize as empty
        self.files = []

     def add_file(self, filepath):
        # Instantiate a HyTextFile, which requires the filepath argument,
        # then add it to the list.
        tracker = HyTextFile(file_path)
        self.files.append(tracker)