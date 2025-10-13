
import hy_tracked_textfiles as hy

def calculate_basic_statistics(file: hy.HyTextFile):
    """
    Calculates basic statistics given a file path.

    Arguments:
        file: HyTextFile entry of a tracked file
    
    Returns:
        Tuple containing, in order:
        • Total number of lines
        • Total number of words
        • Total number of characters (without spaces)
        • Total number of characters which are spaces
        • Average words per line
        • Average characters per word
    """

    path = file.path

    file_number_of_lines = 0
    file_number_of_words = 0
    file_number_of_characters = 0
    file_number_of_spaces = 0

    # Read file line by line (*not* all at once in memory :D)
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            # Remove trailing newline but keep internal spaces
            line = line.rstrip('\n')

            file_number_of_lines += 1

            # Split into words (for simplicity let's just assume a space delimits each word)
            words = line.split(' ')
            line_number_of_words = len(words)

            # Since we split on spaces, we can calculate how many spaces there were via:
            file_number_of_spaces += (len(words) - 1)

            # Count characters in all words (excluding spaces)
            line_number_of_characters = sum(len(word) for word in words)

            # Apply local variables for this line to the file scope
            file_number_of_words += line_number_of_words
            file_number_of_characters += line_number_of_characters

    # Compute averages
    average_words_per_line = file_number_of_words / file_number_of_lines if file_number_of_lines != 0 else 0
    average_characters_per_word = file_number_of_characters / file_number_of_words if file_number_of_words != 0 else 0

    # Return final ordered tuple
    return (
        file_number_of_lines,
        file_number_of_words,
        file_number_of_characters,
        file_number_of_spaces,
        average_words_per_line,
        average_characters_per_word,
    )
