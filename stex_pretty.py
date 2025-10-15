"""

1DV501 Final Project - SimpleTextAnalysis
stex_pretty.py

Author: Daniel Lind

This can be seen as the human-oriented counterpart to stex_json.py,
as both of these files have the purpose of parsing class data and returning
it in another format. Unlike stex_json, this file contains functions
intended to make that content human readable ("pretty".)

"""

import stex_filing as stex

def fetch_basic_statistics(file: stex.TextFile) -> str:
    """
    Returns a printable string containing left/right aligned basic statistics
    for the HyTextFile provided, including:
    Number of Lines, Number of Words, Number of Unique Words, 
    Characters, Average words in a line, characters in a word.
    """
    
    # Initialize a dictionary of stats
    stats = {
        'Number of Lines': file.number_of_lines,
        'Number of Words': file.number_of_words,
        'Unique Words': len(file.get_unique_words()),
        'Characters (excluding spaces)': file.number_of_characters,
        'Characters (including spaces)': file.number_of_characters_and_spaces,
        'Average words in a line': file.get_average_words_per_line(),
        'Average characters in a word': file.get_average_characters_per_word()
    }
    
    result = format_dictionary(stats)
    return result.strip()

def fetch_word_length_statistics(file: stex.TextFile) -> str:
    """
    
    """
    
    shortest_length, longest_length, average_length = file.get_word_length_statistics()
    
    stats = {
        'Shortest word': f'{format_number(shortest_length)} characters',
        'Longest word': f'{format_number(longest_length)} characters',
        'Average word length': f'{str(round(average_length, 3))} characters'
    }
    
    result = format_dictionary(stats)
    return result

def fetch_sentence_statistics(file: stex.TextFile) -> str:
    """

    """
    sentence_count = file.total_sentences
    average = file.get_average_words_per_sentence(2) # Rounding to 2 decimals
    shortest_sentence = file.shortest_sentence_text
    longest_sentence = file.longest_sentence_text

    stats = {
        'Total sentences': f'{format_number(sentence_count)}',
        'Average words per sentence': f'{average}',
        'Shortest sentence': f'{format_number(len(shortest_sentence))} words',
        'Longest sentence': f'{format_number(len(longest_sentence))} words', 
        '': '',
        'Shortest sentence text': f'"{shortest_sentence}"',
        'Longest sentence text': f'"{longest_sentence}"', 
    }

    result = format_dictionary(stats)
    return result

def fetch_word_frequency_list(file: stex.TextFile, top_n_words: int = 10) -> str:
    """
    Given a HyTextFile object, this will return a stylized list of the N 
    most common words on file for that object as well as the amount of 
    occurrences and the % of words that each entry makes up.

    Arguments:
        file: HyTextFile to consider
        n: Top N objects to list. If this exceeds the total amount of unique words, this will be decreased.

    Returns:
        String of the prettied word frequency list.
    """
    # For starters, we'll want to actually fetch these statistics to construct a
    # stylized list. This functionality is handled in the HyTextFile class.
    # The returned dictionary contains the word as a key and the amount of occurrences as a value.
    common_words_dictionary = file.get_top_elements_of_dictionary(file.word_occurrences, top_n_words)

    # To calculate relative percentages, we'll also need to know the amount of words in general.
    total_number_of_words = file.number_of_words

    columns = [
        Column('Rank', '^'),
        Column('Word', '<'),
        Column('Occurrences', '>'),
        Column('Percentage', '>'),
    ]

    rows = []

    # This is just for display purposes - we assign a "ranking" to
    # each entry by enumerating. (Human readable, so index starts at 1)    
    ranked_items = enumerate(common_words_dictionary.items(), start=1)

    for rank, (word, count) in ranked_items:
        # Calculate percentage relative to total number of all words
        percentage = (count / total_number_of_words) * 100
        
        row = create_word_row(rank, word, count, percentage)
        rows.append(row)

    # Generate the table
    table = gen_table(columns, rows)
    
    return table

def fetch_sentence_length_distribution_list(file: stex.TextFile, top_n_sentences: int = 5) -> str:
    """
    Much like the word frequency list, this function will take a
    TextFile object and generate a prettied table-like representation
    of the N most common word/sentence distributions.

    Arguments:
        file: TextFile to consider
        top_n_sentences: How many ranks to return.

    Returns:
        Printable string.
    """
    top_entries = file.get_top_elements_of_dictionary(file.sentence_length_distribution, top_n_sentences)

    columns = [
        Column('Rank', '^'),
        Column('Amount of Words', '>'),
        Column('Count of Sentences', '>')
    ]

    rows = []

    # Assign rankings (as above)
    ranked_items = enumerate(top_entries.items(), start=1)

    for rank, (length, count) in ranked_items:
        row = create_sentence_row(rank, length, count)
        rows.append(row)

    # Generate the table
    table = gen_table(columns, rows)
    return table



#
# Helper functions below.
#

def format_dictionary(dictionary: dict) -> str:
    """
    Given a dictionary, e.g. { 'Title': 'Value'}, returns a printable
    string with the title left-aligned and value right-aligned. If the
    value is an integer, it will be formatted as a string.
    
    Arguments:
        dictionary: the dictionary to consider
    
    Returns:
        Printable string.
    """
    
    # Initialize returned variable
    result = ''
    
    # Iterate through dictionary and add each pair to our stringbuilder,
    # using some f-String shenanigans to align the values to the right.
    for title, value in dictionary.items():
        # If the value is an integer, add comma separators for big numbers.
        if(isinstance(value, int)):
            value = format_number(value)
        result += f'{title:<30}: {value:>10}' + '\n'
        
    return result

def format_number(number: int) -> str:
    """
    Converts an integer to a human-readable string with commas separating
    thousands, millions, etc.
    
    Arguments:
        number: integer to format.
    
    Returns:
        Formatted number as a string.
    """
    return f"{number:,}"

class Column:
    """
    Represents a single column definition in a table.
    """
    def __init__(self, column_name: str, align: str = "<"):
        self.column_name = column_name
        self.align = align  # < = left, ^ = center, > = right
        self.column_min_width = len(column_name)


class Row:
    """
    Represents a single table row, stored as a dict of {columnName: value}.
    """
    def __init__(self, value_pair: dict):
        self.value_pair = value_pair


def gen_table(columns: list[Column], rows: list[Row]) -> str:
    """
    Generates a formatted text table from a list of ColumnObj and RowObj.
    Do note that a lot of this code is adapted from realExercise1.ipynb
    and is just a little ugly because of it.

    Args:
        columns: A list of ColumnObj describing layout and alignment.
        rows: A list of RowObj containing the table data.

    Returns:
        The complete table as a formatted string.
    """
    # Calculate minimum width of each column
    for column in columns:
        for row in rows:
            considered = str(row.value_pair.get(column.column_name, ""))
            if considered:
                column.column_min_width = max(column.column_min_width, len(considered))

    # Build header
    header = "║" + "║".join(
        f" {column.column_name:{column.align}{column.column_min_width}} " for column in columns
    ) + "║"

    # Divider
    divider = ("═" * len(header))

    # Build data rows
    body_lines = []
    for row in rows:
        row_line = "║" + "║".join(
            f" {str(row.value_pair.get(column.column_name, '')):{column.align}{column.column_min_width}} " # TODO: yikes
            for column in columns
        ) + "║"
        body_lines.append(row_line)

    table = "\n".join([divider, header, divider, *body_lines, divider])

    return table

def create_word_row(rank: int, word: str, occurrences: int, percentage: float) -> Row:
    """
    Creates a RowObj containing rankings for a specific entry in a word frequency table.

    Arguments:
        rank: Integer of which rank this word sits at.
        word: The word itself.
        occurrences: The number of times the word occurs.
        percentage: Float representation of a %

    Returns:
        Row
    """
    formatted_occurrences = f"{occurrences:,} times"
    formatted_percentage = f"({percentage:5.2f}%)"
    return Row({
        "Rank": rank,
        "Word": word,
        "Occurrences": formatted_occurrences,
        "Percentage": formatted_percentage
    })

def create_sentence_row(rank: int, length: int, occurrences: int) -> Row:
    """
    Creates a RowObj containing rankings for a specific entry the
    sentence length distribution table.

    Arguments:
        rank: Integer of which rank this length sits at.
        length: The sentence length, in words.
        occurrences: The amount of sentences of that length.

    Returns:
        Row
    """
    formatted_occurrences = f"{occurrences:,} times"
    return Row({
        "Rank": rank,
        "Amount of Words": length,
        "Count of Sentences": occurrences
    })
