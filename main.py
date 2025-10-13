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

# Imports
import os.path   # ...to verify existence of dependency files
import hy_tracked_textfiles as hy   # ...contains classes to track data on files

"""
    Generates a unicode based header for the menu prompt.
    Notice: if header_text exceeds screen size, this may cause graphical issues.

    Args:
        header_text: Contents of header.
        padding: Amount of whitespace on either side of the header_text.

    Returns multiline string of the header, suitable to be passed into print() immediately.
"""
def generated_stylized_content_box(header_text: str, padding: int = 2):
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

def print_menu_prompt(options_menu_content: str):
    # TODO: base width of dividing lines on intro header?
    
    # Print current status as a cool header.
    current_selected = get_current_selected_file()
    status_header_content = "No file is selected. Choose one by selecting S." if current_selected == None else f"Currently working with:\n{current_selected}"
    status_header = generated_stylized_content_box(status_header_content)
    print(status_header)

    print(options_menu_content)

"""
    Helper function.
    When passed a user input from the main menu loop,
    this will normalize it to be lowercase and a single character.
"""
def normalize_user_input(userstr: str):
    # For now, let's allow inputs with a length over 1.
    # This could be useful, since 'Quit' will resolve to 'q' and that's all we care about.
    # On the other hand this could cause confusion, since typing 'quaaludes' will also quit the program...
    
    lowercase_string = userstr.lower()

    if(len(lowercase_string) < 1):
        # Blank input, ignore
        return None
    
    # First character of user string
    return lowercase_string[0]

"""
    Reads a prompt/template file from disk and returns its contents,
    stripping out comments. Raises error if file does not exist

    Arguments:
        template_path: path to the place on disk where the template file is expected to be.
    
    Returns:
        Contents of file located at template_path, with comments stripped.
"""
def get_prompt_file_contents(template_path: str):
    # As a sanity check, make sure the file exists.
    # If the user deleted it, y'know, break.
    # TODO: 'Real' error handling.
    if not os.path.isfile(template_path):
        print (f" *** {template_path} is missing, aborting! *** ")
        raise FileNotFoundError
    
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

def interactive_load_file_prompt(masterFileInventory: hy.HyFileInventory):
    file_to_load = None
    while(file_to_load == None):
        user_input = input("Enter path to text file:")
        try:
            masterFileInventory.add_file(user_input)
        except FileNotFoundError:
            print("No such file could be found.")
        except Exception as e:
            print("Please try again. An unexpected error has occurred: ", e)
    
    # TODO: perform analysis here and save results in the file we just added
    # for now, just return
    print("Successfully loaded file!")
    return


"""
    Primary function to execute user's desired effects.

    Arguments:
        master_file_inventory: HyFileInventory object which tracks file data

        user_choice: single character indicating the action selected in the main menu loop.
        Possibly Values:
            l = load file
            u = unload file
            e = export
            q = quit
            
            b = print basic statistics
            w = print word frequency
            s = print sentence analysis
            c = print char analysis

    Does not return a tangible value - performs action and prints to screen.
"""
def execute(master_file_inventory: hy.HyFileInventory, user_choice: chr):
    match(user_choice):
        case 'l':
            interactive_load_file_prompt(master_file_inventory)

        case 'q':
            # Handled directly in main_menu_loop. Simply return
            return

        case _:
            print('Invalid selection.')
            return

"""
    Main program loop. Handles the general flow of prompting the user and performing actions.
"""
def main_menu_loop():
    # Read the contents of option_prompt.txt into a cached options_menu_content,
    # to avoid reading the file every time we print the menu.
    template_path = 'option_prompt.txt'
    options_menu_content = get_prompt_file_contents(template_path)

    user_choice = ''
    
    # Quit if the user decides to abort program loop.
    while(user_choice != 'q'):
        print_menu_prompt(options_menu_content)

        # Prompt user for selection until it's not blank.
        user_input = None
        while(user_input == None):
            user_input = normalize_user_input(input('>'))
        
        # Prepare "user_choice"
        user_choice = user_input

        # Perform user's decided action 
        execute(user_choice)



"""
    Program entrypoint.
"""
def main():
    intro_header = generated_stylized_content_box(
"""
Welcome to HyTextAnalysis!
You will be shown a TUI menu of different operations.
    
To start, you should probably select a text file.

Happy analyzing!
""")
    
    print(intro_header)

    # Transfer executon to main menu loop. Will return here (and exit) when the user quits.
    main_menu_loop()

    # We have broken out of the main loop - the application will exit.
    return

if __name__ == "__main__":
    main()

    # important note for later: matplotlib works fine in jupyter, inline