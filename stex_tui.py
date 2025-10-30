

# Imports
from stex_exceptions import OperationCancelled
from pathlib import Path
import stex_filing as stex
import os

def generate_stylized_content_box(header_text: str, padding: int = 2) -> str:
    """
    Generates a unicode header for the menu prompt.
    Notice: if header_text exceeds screen width, this may cause graphical issues.

    Args:
        header_text: Contents of header.
        padding: Amount of whitespace on either side of the header_text.

    Returns:
        multiline string of the header, suitable to be passed into print() immediately.
    """
    # This may have trouble displaying on some terminals,
    # but it seems to be fine on JupyterHub.

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

def get_loaded_file_names(inventory: list[stex.TextFile]) -> tuple[str] | None:
    """
    Returns the names of files which are currently selected in a tuple.
    Returns None if no file selected.
    """
    # No files? No tuples. 
    if len(inventory) < 1:
        return None
    
    # Get the name of each file in a list
    names = []
    for file in inventory:
        names.append(file.shortname)
    
    return tuple(names)
    

def print_menu_prompt(options_menu_content: str, inventory: list[stex.TextFile]):
    # TODO: base width of dividing lines on intro header?
    
    # Generate content box for the possibly options. 
    options_menu_content_box = generate_stylized_content_box(options_menu_content)
    print(options_menu_content_box)

    # Print status (i.e. what files are loaded)
    current_selected = get_loaded_file_names(inventory)
    status = "No file is selected. Choose one by selecting <L>." if current_selected == None else f"Currently working with:\n{", ".join(current_selected)}"
    print(status)


def get_prompt_file_contents(template_path: str) -> str:
    """
    Reads a prompt/template file from disk and returns its contents,
    stripping out comments. Raises error if file does not exist

    Arguments:
        template_path: path to the place on disk where the template file is expected to be.
    
    Returns:
        Contents of file located at template_path, with comments stripped.
    """
    # As a sanity check, make sure the file exists.
    # If the user deleted it, y'know, break.
    # TODO: 'Real' error handling.
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f" *** {template_path} is missing, aborting! *** ")
    
    # Since we can reasonable expect the prompt file to be small,
    # we can safely read it into memory.
    f = open(template_path, 'r', encoding='utf-8')
    options_menu_content_raw = f.read()
    f.close()

    # Now, let's flatten comments that may have been in the file.
    options_menu_content = ''
    for line in options_menu_content_raw.split('\n'):
        if len(line) < 1 or line[0] != '#':
            options_menu_content += line + '\n'

    return options_menu_content

def load_file_prompt(inventory: list[stex.TextFile]) -> stex.TextFile:
    """
    Provides an interactive prompt to load a text file by path.
    Appends selected file to provided inventory.
    """
    loaded_file = None
    while loaded_file == None:
        user_input = input("Enter path to text file:")
        try:
            # Cancel if the user just presses Enter.
            if len(user_input) == 0:
                raise OperationCancelled
            
            candidate_file = stex.TextFile(user_input)
            inventory.append(candidate_file)
            loaded_file = candidate_file
        except FileNotFoundError:
            print("No such file could be found.")
        except ValueError:
            print("Please provide a valid .TXT file")
    
    return loaded_file

def save_file_prompt(content: str) -> str:
    """
    Shows an interactive prompt which asks what file to save the contents of 'content' in.
    If the user provides a valid path and doesn't abort, the file will be saved.
    
    Arguments:
        content: file contents
    
    Returns:
        Chosen path to saved file.
    """
    
    chosen_path = ''
    while chosen_path == '':
        # Prompt for file path.
        user_input = input('Please enter the path where you wish to export the file (e.g., /tmp/working_data.json). Enter "Cancel" to abort.\n> ')
        if user_input.lower() == 'cancel':
            raise OperationCancelled

        # If the file already exists, confirm whether or not they want to override it.
        if os.path.exists(user_input):
            verification_input = input(f'There is already a file at {user_input}. Would you like to replace it? (y/N)\n> ')
            if not verification_input.lower() == 'y':
                continue
        
        chosen_path = user_input
    
    # Write data to file.
    with open(chosen_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return chosen_path

def select_file_prompt(inventory: list[stex.TextFile]) -> stex.TextFile:
    """
    A generic function called from any other function which needs the user
    to select one of the currently loaded files via an interactive prompt.

    Returns:
        HyTextFile object.
    """
    print("==========================")
    print("C. Cancel Operation")

    # List every tracked file and ask them which one to remove.
    number_of_files = len(inventory)
    for i in range(number_of_files):
        print(f"{i}. {inventory[i].shortname}")
        
    print("==========================")
    user_choice = -1
    # Loop until the user provides a valid choice which is inbounds
    while user_choice < 0 or user_choice >= number_of_files:
        user_input = input("Enter index of file to choose >")

        # Special case - if the user aborts... abort.
        if user_input.lower() == 'c':
            raise OperationCancelled
        
        # Otherwise, make sure it's in range (keep looping if it isn't)
        try:
            user_choice = int(user_input)
            if user_choice >= number_of_files or user_choice < 0:
                raise ValueError
        except:
            print("You must select an index corresponding to a loaded file.")
    return inventory[user_choice]

def list_text_files() -> str:
    """
    Lists the files in the current working directory and returns a string
    of all files ending in .txt, separated by newline
    """
    txt_files = []

    for path in Path('.').rglob('*.txt'):
        txt_files.append(str(path))

    return '\n'.join(txt_files)
