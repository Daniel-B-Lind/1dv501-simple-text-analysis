# pyright: reportPossiblyUnboundVariable=false
"""

1DV501 Final Project - SimpleTextAnalysis
stex_main.py

Author: Daniel Lind

This file is the entrypoint for the SimpleTextAnalysis project.
It is the only file focusing on the interactive user interface,
delegating functionality to other imports.

As of now, it is responsibly for TUI elements as well as actual interaction.
In the future, the TUI helpers may be moved to another file.

"""

# Imports
from sys import exit # ...to gracefully exit
import os.path   # ...to verify existence of dependency files
from pathlib import Path  # ...for text file search and display
import stex_filing as stex   # ...contains classes to track data on files
import stex_json as serializer   # ...contains functions to serialize/deserialize data
import stex_analysis as analyse
import stex_plotting as plot # ...contains all matplotlib shenanigans
import stex_pretty as pretty  # ...to get human-readable results
import stex_tui as tui # ...for terminal user interface
from stex_exceptions import OperationCancelled # ...custom exception

def _analyze_all(loaded_file: stex.TextFile) -> None:
    print("Successfully loaded file! Starting analysis.")
    
    print(" [1] Performing basic analysis... ", end='')
    basic_statistics = analyse.invoke_basic_statistics(loaded_file)
    loaded_file.append_basic_statistics(basic_statistics)
    print("done!")

    print(" [2] Performing word frequency analysis... ", end='')
    word_statistics = analyse.invoke_word_frequency_statistics(loaded_file)
    loaded_file.append_word_frequency_statistics(word_statistics)
    print("done!")

    print(" [3] Performing sentence analysis... ", end='')
    sentence_statistics = analyse.invoke_sentence_statistics(loaded_file)
    loaded_file.append_sentence_statistics(sentence_statistics)
    print("done!")

    print(" [4] Performing character analysis... ", end='')
    character_statistics = analyse.invoke_character_statistics(loaded_file)
    loaded_file.append_character_statistics(character_statistics)
    print("done!")
    
    print(" [5A] Performing trigram analysis... ", end='')
    trigram_statistics = analyse.invoke_trigram_analysis(loaded_file)
    print("done!")
    print(" [5B] Finding closest matching language...", end='')
    language_probabilities = analyse.invoke_find_closest_trigram_sample(trigram_statistics)
    loaded_file.append_language_probabilities(language_probabilities)
    print("done!")

    print("All analysis passes completed without issue.")


def _normalize_user_input(userstr: str) -> str | None:
    """
    Helper function.
    When passed a user input from the main menu loop,
    this will normalize it to be lowercase and a single character.
    """
    # For now, let's allow inputs with a length over 1.
    # This could be useful, since 'Quit' will resolve to 'q' and that's all we care about.
    # On the other hand this could cause confusion, since typing 'quaaludes' will also quit the program...
    
    lowercase_string = userstr.lower()

    if len(lowercase_string) < 1:
        # Blank input, ignore
        return None
    
    # First character of user string
    return lowercase_string[0]

def execute(master_file_inventory: list[stex.TextFile], user_choice: str) -> None:
    """
    Primary function to execute user's desired effects.

    Arguments:
        master_file_inventory: List of TextFile objects

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
            
            i = identify language
            2 = word frequency comparison 2 files

    Does not return a value - delegates action and prints to screen.
    """
    
    # If the operation we're planning to do requires a file, select one.
    CHOICES_REQUIRING_LOADED_FILE = set('uebwmsci')
    if user_choice in CHOICES_REQUIRING_LOADED_FILE:
        try:
            selected_file = _prepare_to_request_result(master_file_inventory)
        except OperationCancelled:
            print("Cancelled.")
            return
        except ValueError:
            print("No files are loaded! Load one with <L>")
            return

    match(user_choice):
        # - Meta -
        case 'd': # Display files in current directory
            text_files = tui.list_text_files()
            print(text_files)
            return

        case 'l': # Load file
            try:
                loaded_file = tui.load_file_prompt(master_file_inventory)
            except OperationCancelled:
                print("Cancelled.")
                return
            
            # Performs all exercise passes and saves data ("ingests" file)
            _analyze_all(loaded_file)
            return

        case 'u': #Unload file
            result = _unload_file(master_file_inventory, selected_file)
            print(result)
            return

        case 'e': # Export results
            print("Serializing results...", end='')
            full_data_dump = serializer.serialize_all(selected_file)
            print("done!")
            
            try:
                result = tui.save_file_prompt(full_data_dump)
                print(f"Successfully exported data to file at {result}!")
            except OperationCancelled:
                print("Cancelled.")
            except PermissionError:
                print("You do not have permission to write to that file.")
            except:
                print("An unexpected error occurred while attempting to export the data.")
            
            return

        case 'q': # Quit
            # Handled directly in menu_loop. Simply return.
            print("Goodbye!")
            return

        # - Simple Analysis Queries - 
        case 'b': # Basic statistics
            result = pretty.fetch_basic_statistics(selected_file)
            print(result)
            plot.plot_basic_analysis(selected_file)
            return
        
        case 'w': # Word frequency statistics
            frequency_table = pretty.fetch_word_frequency_table(selected_file)
            print(frequency_table)
            
            length_stats = pretty.fetch_word_length_statistics(selected_file)
            print(length_stats)
            
            orphan_word_count = len(selected_file.get_orphan_words())
            print(f'Words appearing only once: {pretty._format_number(orphan_word_count)}')
            
            plot.plot_word_analysis(selected_file, 10)
            return
        
        case 's': # Sentence analysis
            frequency_table = pretty.fetch_sentence_length_distribution_table(selected_file)
            print(frequency_table)
            sentence_stats = pretty.fetch_sentence_statistics(selected_file)
            print(sentence_stats)
            
            plot.plot_sentence_analysis(selected_file)
            return

        case 'c': # Character analysis
            letter_frequency_table = pretty.fetch_common_letters_list(selected_file)
            print(letter_frequency_table)
            letter_type_distribution_table = pretty.fetch_character_type_distribution_table(selected_file)
            print(letter_type_distribution_table)
            
            plot.plot_character_analysis(selected_file, 10)
            return
        
        case 'i': # Identify language
            language_probability_table = pretty.fetch_language_guess_table(selected_file)
            print(language_probability_table)
            plot.plot_language_confidence(selected_file)
            return
        
        case 'm': # Measure similarity between unique word distribution
            # Note - while we already have a selected_file, this will require a 2nd selection.
            print(f'Select file to compare with {selected_file.path}:')
            try:
                selected_file_b = tui.select_file_prompt(master_file_inventory)
            except OperationCancelled:
                print('Cancelled.')
                return
            
            # Minor violation - we're gonna make a call directly to analyse.invoke[...] here,
            # because this is by nature not something we can possibly do during ingest.
            cosine_similarity = analyse.invoke_cosine_similarity(selected_file.word_occurrences, selected_file_b.word_occurrences)
            result = pretty.fetch_similarity_two_files(cosine_similarity)
            print(result)

        case _:
            print('Invalid selection or option not yet implemented.')
            return


def _prepare_to_request_result(inventory: list[stex.TextFile]) -> stex.TextFile:
    """
    Query the user on which file they want the results of. If only one file is available,
    automatically chooses it.

    If no files are loaded, returns None.
    """

    if len(inventory) == 0:
        # There's nothing to return the results of...
        raise ValueError("Inventory contains no HyTextFile objects!")
    elif len(inventory) == 1:
        # If there's only a single loaded file, we don't want to bother the user since
        # they only have one choice anyway.
        return inventory[0]

    # Alright, if we're here, we do actually have to prompt the user.
    return tui.select_file_prompt(inventory)

def _unload_file(inventory: list[stex.TextFile], file_to_remove: stex.TextFile) -> str:
    # Remove from inventory
    try:
        inventory.remove(file_to_remove)
    except:
        return "An unexpected error occurred while attempting to unload that file."
    
    return 'Successfully unloaded file!'


def menu_loop(main_inventory: list[stex.TextFile]):
    """
    Main program loop. Handles the general flow of prompting the user and performing actions.
    """
    # Read the contents of option_prompt.txt into a cached options_menu_content,
    # to avoid reading the file every time we print the menu.
    template_path = 'resources/option_prompt.txt'
    options_menu_content = tui.get_prompt_file_contents(template_path)

    user_choice = ''
    
    # Quit if the user decides to abort program loop.
    while user_choice != 'q':
        try:
            tui.print_menu_prompt(options_menu_content, main_inventory)

            # Prompt user for selection until it's not blank.
            user_input = None
            while user_input == None:
                user_input = _normalize_user_input(input('> '))
            
            # Prepare "user_choice"
            user_choice = user_input

            # Perform user's decided action 
            execute(main_inventory, user_choice)

            # Hold for user input.
            _ = input("\nPress enter to continue...")
        except KeyboardInterrupt:
            print('\nCtrl+C detected, exiting...\n')
            exit()

def main():
    """
    Program entrypoint.
    """
    welcome_prompt = tui.get_prompt_file_contents("resources/welcome_prompt.txt")
    intro_header = tui.generate_stylized_content_box(welcome_prompt)
    
    print(intro_header)

    # Instantiate the main list  of TextFiles
    main_inventory = []

    # Transfer executon to main menu loop. Will return here (and exit) when the user quits.
    menu_loop(main_inventory)

    # We have broken out of the main loop - the application will exit.
    return

if __name__ == "__main__":
    main()