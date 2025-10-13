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
from sys import exit # ...to gracefully exit
import os.path   # ...to verify existence of dependency files
import hy_tracked_textfiles as hy   # ...contains classes to track data on files
import hy_fetch_json as result_handler   # ...contains functions to serialize/deserialize data
import hy_analysis as analyse

# Custom exception
class OperationCancelled(Exception):
    """
    Raised when a user explicitly chooses to abort or cancel an operation 
    mid-execution.
    """
    def __init__(self, message="Operation was cancelled by the user."):
        self.message = message
        super().__init__(self.message)

def generated_stylized_content_box(header_text: str, padding: int = 2) -> str:
    """
    Generates a unicode header for the menu prompt.
    Notice: if header_text exceeds screen width, this may cause graphical issues.

    Args:
        header_text: Contents of header.
        padding: Amount of whitespace on either side of the header_text.

    Returns:
        multiline string of the header, suitable to be passed into print() immediately.
    """
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

def get_loaded_file_names(inventory: hy.HyFileInventory) -> tuple[str]:
    """
    Returns the names of files which are currently selected in a tuple.
    Returns None if no file selected.
    """
    # No files? No tuples. 
    if(len(inventory.files) < 1):
        return None
    
    # Get the name of each file in a list
    names = []
    for file in inventory.files:
        names.append(file.shortname)
    
    return tuple(names)
    

def print_menu_prompt(options_menu_content: str, inventory: hy.HyFileInventory):
    # TODO: base width of dividing lines on intro header?
    
    # Generate content box for the possibly options. 
    options_menu_content_box = generated_stylized_content_box(options_menu_content)
    print(options_menu_content_box)

    # Print status (i.e. what files are loaded)
    current_selected = get_loaded_file_names(inventory)
    status = "No file is selected. Choose one by selecting <L>." if current_selected == None else f"Currently working with:\n{", ".join(current_selected)}"
    print(status)

def normalize_user_input(userstr: str) -> str:
    """
    Helper function.
    When passed a user input from the main menu loop,
    this will normalize it to be lowercase and a single character.
    """
    # For now, let's allow inputs with a length over 1.
    # This could be useful, since 'Quit' will resolve to 'q' and that's all we care about.
    # On the other hand this could cause confusion, since typing 'quaaludes' will also quit the program...
    
    lowercase_string = userstr.lower()

    if(len(lowercase_string) < 1):
        # Blank input, ignore
        return None
    
    # First character of user string
    return lowercase_string[0]

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

def interactive_load_file_prompt(inventory: hy.HyFileInventory):
    loaded_file = None
    while(loaded_file == None):
        user_input = input("Enter path to text file:")
        try:
            loaded_file = inventory.add_file(user_input)
        except FileNotFoundError:
            print("No such file could be found.")
        except ValueError:
            print("Please provide a valid .TXT file")
        except Exception as e:
            print("Please try again. An unexpected error has occurred: ", e)
    

    print("Successfully loaded file! Starting analysis.")
    
    print(" [1] Performing basic analysis... ", end='')
    basic_statistics = analyse.calculate_basic_statistics(loaded_file)
    loaded_file.append_basic_statistics(basic_statistics)
    print("done!")
    
    # TODO: perform analysis here and save results in the file we just added
    # for now, just return
    print("Ooops, no further functionality exists yet. Pretend I did it!")
    return

def interactive_unload_file_prompt(inventory: hy.HyFileInventory):
    # If there aren't any files which are tracked, then there's nothing to unload.
    if(len(inventory.files) < 1):
        print("There aren't any loaded files to unload.")
        return
    
    file = select_file_prompt(inventory)
    
    # If the operation was canceled, return early.
    if file == None:
        return

    # Remove from inventory
    try:
        inventory.files.remove(file)
    except:
        print("An unexpected error occurred while attempting to unload that file.")
        return
    
    print(f"Successfully unloaded file!")

def select_file_prompt(inventory: hy.HyFileInventory) -> hy.HyTextFile:
    """
    A generic function called from any other function which needs the user
    to select one of the currently loaded files via an interactive prompt.

    Returns:
        HyTextFile object.
    """
    print("==========================")
    print("C. Cancel Operation")

    # List every tracked file and ask them which one to remove.
    number_of_files = len(inventory.files)
    for i in range(number_of_files):
        print(f"{i}. {inventory.files[i].shortname}")
    print("==========================")
    user_choice = -1
    # Loop until the user provides a valid choice which is inbounds
    while(user_choice < 0 or user_choice >= number_of_files):
        user_input = input("Enter index of file to choose >")

        # Special case - if the user aborts, return None early.
        if(user_input.lower() == 'c'):
            return None
        
        # Otherwise, make sure it's in range (keep looping if it isn't)
        try:
            user_choice = int(user_input)
            if(user_choice >= number_of_files or user_choice < 0):
                raise ValueError
        except:
            print("You must select an index corresponding to a loaded file.")
    return inventory.files[user_choice]

def prepare_to_request_result(inventory: hy.HyFileInventory) -> list[hy.HyTextFile]:
    """
    Query the user on which file they want the results of. If only one file is available,
    automatically chooses it.

    If no files are loaded, returns None.
    """

    if(len(inventory.files) == 0):
        # There's nothing to return the results of...
        raise ValueError("Inventory contains no HyTextFile objects!")
    elif(len(inventory.files) == 1):
        # If there's only a single loaded file, we don't want to bother the user since
        # they only have one choice anyway.
        return inventory.files[0]

    # Alright, if we're here, we do actually have to prompt the user.
    return select_file_prompt(inventory)

def list_text_files() -> str:
    """
    Lists the files in the current working directory and returns a string
    of all files ending in .txt, separated by newline
    """
    file_list = os.listdir('.')
    file_list_clean = ''
    for file in file_list:
        if file.endswith('.txt'):
            file_list_clean += (file + '\n')
    return file_list_clean.strip()

def execute(master_file_inventory: hy.HyFileInventory, user_choice: chr):
    """
    Primary function to execute user's desired effects.

    Arguments:
        master_file_inventory: HyFileInventory object which tracks file data

        user_choice: single character indicating the action selected in the main menu loop.
        Possibly Values:
            d = display files in dir
            l = load file
            u = unload file
            e = export
            q = quit
            
            b = print basic statistics
            w = print word frequency
            s = print sentence analysis
            c = print char analysis

    Does not return a value - delegates action and prints to screen.
    """

    match(user_choice):
        
        # - Meta -
        case 'd': # Display files in current directory
            text_files = list_text_files()
            print(text_files)
            return

        case 'l': # Load file
            interactive_load_file_prompt(master_file_inventory)
            return

        case 'u': #Unload file
            interactive_unload_file_prompt(master_file_inventory)    
            return

        case 'e': # Export results
            print("Not yet implemented!")
            return

        case 'q': # Quit
            # Handled directly in menu_loop. Simply return.
            print("Goodbye!")
            return

        # - Simple Analysis Queries - 
        case 'b': # Basic statistics
            try:
                textfiles = prepare_to_request_result(master_file_inventory)
            except OperationCancelled:
                print("Cancelled.")
                return
            except ValueError:
                print("Load a file first.")
                return

            json_result = result_handler.fetch_basic_statistics(textfiles)
            pretty_result = result_handler.json_to_pretty(json_result)
            
            print(pretty_result)
            return

        case _:
            print('Invalid selection or option not yet implemented.')
            return

def menu_loop(main_inventory: hy.HyFileInventory):
    """
    Main program loop. Handles the general flow of prompting the user and performing actions.
    """
    # Read the contents of option_prompt.txt into a cached options_menu_content,
    # to avoid reading the file every time we print the menu.
    template_path = 'option_prompt.txt'
    options_menu_content = get_prompt_file_contents(template_path)

    user_choice = ''
    
    # Quit if the user decides to abort program loop.
    while(user_choice != 'q'):
        try:
            print_menu_prompt(options_menu_content, main_inventory)

            # Prompt user for selection until it's not blank.
            user_input = None
            while(user_input == None):
                user_input = normalize_user_input(input('>'))
            
            # Prepare "user_choice"
            user_choice = user_input

            # Perform user's decided action 
            execute(main_inventory, user_choice)

            # Hold for user input.
            _ = input("Press enter to continue...")
        except KeyboardInterrupt:
            print('\nCtrl+C detected, exiting...\n')
            exit()

def main():
    """
    Program entrypoint.
    """
    welcome_prompt = get_prompt_file_contents("welcome_prompt.txt")
    intro_header = generated_stylized_content_box(welcome_prompt)
    
    print(intro_header)

    # Instantiate the main inventory of text files
    main_inventory = hy.HyFileInventory()

    # Transfer executon to main menu loop. Will return here (and exit) when the user quits.
    menu_loop(main_inventory)

    # We have broken out of the main loop - the application will exit.
    return

if __name__ == "__main__":
    main()

    # important note for later: matplotlib works fine in jupyter, inline