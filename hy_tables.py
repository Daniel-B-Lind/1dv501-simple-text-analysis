"""

1DV501 Final Project - HyTextAnalysis
hy_tables.py

Author: Daniel Lind

Originally created to generate a table of dinosaur data for realExercise1.ipynb,
now retrofitted to create generate Generic Text-Based Tables.

"""
class ColumnObj:
    """
    Represents a single column definition in a table.
    """
    def __init__(self, columnName: str, align: str = "<"):
        self.columnName = columnName
        self.align = align  # < = left, ^ = center, > = right
        self.columnMinWidth = len(columnName)


class RowObj:
    """
    Represents a single table row, stored as a dict of {columnName: value}.
    """
    def __init__(self, valuePair: dict[str, any]):
        self.valuePair = valuePair


def gen_table(columns: list[ColumnObj], rows: list[RowObj]) -> str:
    """
    Generates a formatted text table from a list of ColumnObj and RowObj.

    Args:
        columns: A list of ColumnObj describing layout and alignment.
        rows: A list of RowObj containing the table data.

    Returns:
        The complete table as a formatted string.
    """
    # Calculate minimum width of each column
    for cObj in columns:
        for rObj in rows:
            considered = str(rObj.valuePair.get(cObj.columnName, ""))
            if considered:
                cObj.columnMinWidth = max(cObj.columnMinWidth, len(considered))

    # Build header
    header = "|" + "|".join(
        f" {cObj.columnName:{cObj.align}{cObj.columnMinWidth}} " for cObj in columns
    ) + "|"

    # Divider
    divider = "-" * len(header)

    # Build data rows
    body_lines = []
    for rObj in rows:
        row_line = "|" + "|".join(
            f" {str(rObj.valuePair.get(cObj.columnName, '')):{cObj.align}{cObj.columnMinWidth}} "
            for cObj in columns
        ) + "|"
        body_lines.append(row_line)

    table = "\n".join([header, divider, *body_lines])

    return table

def create_word_row(rank: int, word: str, occurrences: int, percentage: float) -> RowObj:
    """
    Creates a RowObj containing rankings for a specific entry in a word frequency table.

    Arguments:
        rank: Integer of which rank this word sits at.
        word: The word itself.
        occurrences: The number of times the word occurs.
        percentage: Float representation of a %

    Returns:
        RowObj

    """
    formatted_occurrences = f"{occurrences:,} times"
    formatted_percentage = f"({percentage:5.2f}%)"
    return RowObj({
        "Rank": rank,
        "Word": word,
        "Occurrences": formatted_occurrences,
        "Percentage": formatted_percentage
    })
