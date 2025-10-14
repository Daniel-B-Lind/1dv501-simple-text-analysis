"""

1DV501 Final Project - HyTextAnalysis
hy_tables.py

Author: Daniel Lind

Originally created to generate a table of dinosaur data for realExercise1.ipynb,
now retrofitted to create generate Generic Text-Based Tables. 

"""
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
    def __init__(self, value_pair: dict[str, any]):
        self.value_pair = value_pair


def gen_table(columns: list[Column], rows: list[Row]) -> str:
    """
    Generates a formatted text table from a list of ColumnObj and RowObj.

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
            f" {str(row.value_pair.get(column.column_name, '')):{column.align}{column.column_min_width}} "
            for column in columns
        ) + "║"
        body_lines.append(row_line)

    table = "\n".join([divider, header, divider, *body_lines])

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
