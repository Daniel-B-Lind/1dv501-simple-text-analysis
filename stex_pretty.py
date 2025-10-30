"""

1DV501 Final Project - SimpleTextAnalysis
stex_pretty.py

Author: Daniel Lind

This can be seen as the human-oriented counterpart to stex_json.py,
as both of these files have the purpose of parsing class data and returning
it in another format. Unlike stex_json, this file contains functions
intended to make that content human readable ("pretty".)

"""

# Imports
import string
import stex_filing as stex

def fetch_basic_statistics(file: stex.TextFile) -> str:
    """
    Returns a printable string containing left/right aligned basic statistics
    for the TextFile provided, including:
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
    
    result = _format_dictionary(stats)
    return result.strip()

def fetch_word_length_statistics(file: stex.TextFile) -> str:
    """
    Returns a printable pretty string containing containing
    word length statistics such as the shortest word length, 
    longest word length, and the average word length. 
    """
    
    shortest_length, longest_length, average_length = file.get_word_length_statistics()
    
    stats = {
        'Shortest word': f'{_format_number(shortest_length)} characters',
        'Longest word': f'{_format_number(longest_length)} characters',
        'Average word length': f'{str(round(average_length, 3))} characters'
    }
    
    result = _format_dictionary(stats)
    return result

def fetch_sentence_statistics(file: stex.TextFile) -> str:
    """
    Returns a printable pretty string of sentence statistics
    (total sentences, average words per sentence, shortest sentence (length & content),
    longest sentence (length & content))
    """
    sentence_count = file.total_sentences
    average = file.get_average_words_per_sentence(2) # Rounding to 2 decimals
    shortest_sentence = file.shortest_sentence_text
    longest_sentence = file.longest_sentence_text

    stats = {
        'Total sentences': f'{_format_number(sentence_count)}',
        'Average words per sentence': f'{average}',
        'Shortest sentence': f'{_format_number(len(shortest_sentence))} words',
        'Longest sentence': f'{_format_number(len(longest_sentence))} words', 
        '': '', # Blank line, for readability.
        'Shortest sentence text': f'"{shortest_sentence}"',
        'Longest sentence text': f'"{longest_sentence}"', 
    }

    result = _format_dictionary(stats)
    return result

def fetch_character_type_distribution_table(file: stex.TextFile) -> str:
    """
    Returns a printable string containing a table which shows
    the distribution of character types (letters, digits, spaces, punctuation, other)
    in the provided TextFile object.
    """
    
    lowercase_count, uppercase_count = file.get_count_of_lowercase_and_capitalized_ascii()
    # Even though there are likely to be more characters (non-ASCII),
    # stored as file.letter_count, we only want to consider the total 
    # of the letters we actually care about the casing of.
    total_ascii_casing = lowercase_count + uppercase_count 
    
    stats = {
        'Letters': file.letter_count,
        'Digits': file.digit_count,
        'Spaces': file.space_count,
        'Punctuation': file.punctuation_count,
        'Other': file.other_count
    }
    
    total_characters = file.total_characters
    
    columns = [
        Column('Type', '<'),
        Column('Occurrences', '>'),
        Column('Percentage', '>')
    ]
    
    rows = []
    
    for char_type, occurrences in stats.items():
        percentage = (occurrences / total_characters) * 100
        
        row = _create_character_row(char_type, occurrences, percentage)
        rows.append(row)
    
    # Add miscellaneous casing rows which don't play nice with total_characters
    casing_stats = {
        'Uppercase': uppercase_count,
        'Lowercase': lowercase_count
    }
    
    rows_b = []
    
    for casing_type, count in casing_stats.items():
        percentage = (count / total_ascii_casing) * 100
        
        row = _create_character_row(casing_type, count, percentage)
        rows_b.append(row)
    
    table = _gen_table(columns, rows)
    table_b = _gen_table(columns, rows_b)
    return table + '\n' + table_b


def fetch_word_frequency_table(file: stex.TextFile, top_n_words: int = 10) -> str:
    """
    Given a TextFile object, this will return a stylized list of the N 
    most common words on file for that object as well as the amount of 
    occurrences and the % of words that each entry makes up.

    Arguments:
        file: TextFile to consider
        n: Top N objects to list. If this exceeds the total amount of unique words, this will be decreased.

    Returns:
        String of the prettied word frequency list.
    """
    # For starters, we'll want to actually fetch these statistics to construct a
    # stylized list. This functionality is handled in the TextFile class.
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
        
        row = _create_word_row(rank, word, count, percentage)
        rows.append(row)

    # Generate the table
    table = _gen_table(columns, rows)
    
    return table

def fetch_sentence_length_distribution_table(file: stex.TextFile, top_n_sentences: int = 5) -> str:
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
        row = _create_sentence_row(rank, length, count)
        rows.append(row)

    # Generate the table
    table = _gen_table(columns, rows)
    return table

def fetch_common_letters_list(file: stex.TextFile, top_n_letters: int = 10) -> str:

    constraint = set(string.ascii_letters)
    top_letters = file.get_top_elements_of_dictionary(file.character_occurrences, top_n_letters, constraint)
    total_letters = file.letter_count

    columns = [
        Column('Rank', '^'),
        Column('Word', '>'),
        Column('Occurrences', '<'),
        Column('Percentage', '>')
    ]

    rows = []

    ranked_items = enumerate(top_letters.items(), start=1)

    for rank, (letter, count) in ranked_items:
        # Calculate percentage relative to total number of other letters
        percentage = (count / total_letters) * 100
        
        row = _create_word_row(rank, letter, count, percentage)
        rows.append(row)

    # Generate the table
    table = _gen_table(columns, rows)
    return table

def fetch_language_guess_table(file: stex.TextFile, top_n_languages: int = 5) -> str:
    """
    Generates a table containing the most probable language matches
    for the text.
    
    Arguments:
        top_n_languages: The amount of probabilities to show (descending from most probable match)
    
    Returns:
        Printable string
    """
    top_entries = file.get_top_elements_of_dictionary(file.language_probabilities, top_n_languages)

    columns = [
        Column('Language', '<'),
        Column('Probability', '>')
    ]

    rows = []

    for language, float_percentage in top_entries.items():
        row = _create_language_row(language, float_percentage)
        rows.append(row)

    # Generate the table
    table = _gen_table(columns, rows)
    return table

def fetch_similarity_two_files(similarity: float) -> str:
    """
    This 'fetch' is unique because it takes a value directly,
    because the result of a cosine-similarity between two files
    is not stored in either file.
    
    With that said, given a computed similarity, this produces a
    printable string.
    
    Arguments:
        similarity: cosine similarity vlaue between two text files, float
    
    Returns:
        Printable string
    """
    percentage_printable = f'{similarity*100}%'
    return f'Compared files. Similarity: {percentage_printable}'
    

#
# Helper functions below.
#

def _format_dictionary(dictionary: dict) -> str:
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
            value = _format_number(value)
        result += f'{title:<30}: {value:>10}' + '\n'
        
    return result

def _format_number(number: int) -> str:
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


def _gen_table(columns: list[Column], rows: list[Row]) -> str:
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

def _create_word_row(rank: int, word: str, occurrences: int, percentage: float) -> Row:
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

def _create_sentence_row(rank: int, length: int, occurrences: int) -> Row:
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
        "Count of Sentences": formatted_occurrences
    })

def _create_character_row(char_type: str, occurrences: int, percentage: float) -> Row:
    """
    Creates a RowObj containing rankings for a specific entry in a
    character type distribution table.

    Arguments:
        char_type: Character type (letter, digit, punctuation)
        occurrences: Amount of characters of that type.
        percentage: Floating point representation of a percentage

    Returns:
        Row
    """
    formatted_occurrences = f"{occurrences:,} times"
    formatted_percentage = f"({percentage:5.2f}%)"
    return Row({
        "Type": char_type,
        "Occurrences": formatted_occurrences,
        "Percentage": formatted_percentage,
    })

def _create_language_row(language: str, float_percentage: float) -> Row:
    """
    Creates a RowObj for an entry in the language probability table.
    
    Arguments:
        language: string of the language name
        float_percentage: float repesentation of the match for that particular language (E.g. 0.8624)
    
    Returns:
        Row
    """
    formatted_percentage = f"({(float_percentage*100):5.2f}%)"
    return Row({
        "Language": language,
        "Probability": formatted_percentage
    })