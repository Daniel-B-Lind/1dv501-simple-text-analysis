"""

1DV501 Final Project - HyTextAnalysis
main.py

Author: Daniel Lind

This file is the entrypoint for the HyTextAnalysis project.
It is the only file focusing on the interactive user interface,
delegating functionality to other imports.

As of now, it is responsibly for TUI elements as well as actual interaction.
In the future, the TUI helpers may be moved to another file.

"""

"""
    Generates a unicode based header for the menu prompt.
    Notice: if header_text exceeds screen size, this may cause graphical issues.

    Args:
        header_text: Contents of header.
        padding: Amount of whitespace on either side of the header_text.

    Returns multiline string of the header, suitable to be passed into print() immediately.
"""
def generate_header(header_text: str, padding: int = 2):
    # This may have trouble displaying on Jupyter.
    # For now, I am testing this in VSCode.
    # TODO: Evaluate viability on JupyterHub.

    # Split header text on newlines
    text_split = header_text.split('\n')

    # Find longest line
    length_of_longest = 0
    for line in text_split:
        if len(line) > length_of_longest:
            length_of_longest = len(line)
    
    #Calculate required width, not accounting for frame edges
    width = length_of_longest + (padding * 2)

    # Contents of header are our return value
    header = '╔' + ('═' * width) +  '╗' + '\n'

    # For every line, calculate required extra padding and append to final string
    # TODO: This is kind of ugly, should be using f-strings instead..
    for line in text_split:
        header += '║' + (' ' * padding) + line + (' ' * (width - padding - len(line))) + '║' + '\n'
    header += '╚' + ('═' * width) +  '╝' + '\n'

    return header

"""
    [!] this will be moved into another file eventually [!]

    Returns the path to the file which is currently selected for analysis.
    Returns None if no file selected.
"""
def get_current_selected_file():
    # NYI
    return None

def print_menu_prompt():
    # TODO: base width of dividing lines on intro header?
    print("═════════════════════════")
    print("[S]elect Text File")
    print("═════════════════════════")
    

def main():
    intro_header = generate_header(
"""
Welcome to HyTextAnalysis!
You will be shown a TUI menu of different operations.
    
To start, you should probably select a text file.

Happy analyzing!
""")
    
    print(intro_header)

    # Print prompt
    print_menu_prompt()
    pass

if __name__ == "__main__":
    main()

    # important note for later: matplotlib works fine in jupyter, inline