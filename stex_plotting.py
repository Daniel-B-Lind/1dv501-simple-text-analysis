"""
1DV501 Final Project - SimpleTextAnalysis
stex_plotting.py

Author: Daniel Lind 

This file contains all functionality related to matplotlib.

Function Prefix Legend:
    plot_* : Generates and shows a matplotlib figure.

"""

# Imports
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import stex_filing as stex

def plot_basic_analysis(file: stex.TextFile) -> None:
    """
    Plots basic statistics: number of lines, words, characters, and spaces.
    Also shows a pie chart of characters vs spaces. 
    Does not return - shows matplotlib graph.

    Arguments:
        file: TextFile object to analyze
    """

    # Fetch data
    number_of_lines = file.number_of_lines
    number_of_words = file.number_of_words
    number_of_characters = file.number_of_characters
    number_of_spaces = file.number_of_spaces

    # Prepare figure with 1 row, 2 columns.
    # One of these columns will be our bar chart, the other will be the pie chart.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # For text composition, we'll a basic bar chart.
    # Define categories/values
    categories = ['Lines', 'Words', 'Characters', 'Spaces']
    values = [number_of_lines, number_of_words, number_of_characters, number_of_spaces]

    # Give the figure's first column a bar chart and populate it
    ax1.bar(categories, values, edgecolor='black')
    # Name the columns
    ax1.set_title('Text Composition')
    ax1.set_ylabel('Count')

    # For our characters vs. spaces comparison, we'll use a pie chart.
    # Define labels/sizes
    pie_labels = ['Characters (no spaces)', 'Spaces']
    pie_sizes = [number_of_characters, number_of_spaces]

    # Avoiding label/% overlap in pie charts was a rather annoying problem.
    # I adapted some results from https://stackoverflow.com/questions/23577505/how-to-avoid-overlapping-of-labels-autopct-in-a-pie-chart
    # and ultimately decided to use a legend for wedge names and substitute the labels with percentages.
    # TODO: Accessibility issue, as this relies on the user being able to tell colors apart.
    wedges, _, _= ax2.pie(
        pie_sizes,
        autopct='%1.1f%%', # percentages rounded to 1 decimal point
        startangle=90,
        wedgeprops={'edgecolor':'black'},
        pctdistance=1.2    # offsets percentages to be outside of the pie chart
    )

    # Set 2nd columns title, legend, etc.
    ax2.set_title('Character Type Distribution')
    ax2.legend(wedges, pie_labels, title='Categories', loc='center left', bbox_to_anchor=(1.2, 0.5))
    ax2.set_aspect('equal') 
    ax2.axis('off')

    # Display figure
    plt.tight_layout()
    plt.show()


def plot_word_analysis(file: stex.TextFile, top_n: int = 10) -> None:
    """
    Plots the most common words and a histogram of word lengths.
    Does not return - shows matplotlib figure.

    Arguments:
        file: TextFile object
        top_n: number of top words to display
    """
    # Define figure with two columns
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

    # Get data from textfile object
    top_words_dict = file.get_top_elements_of_dictionary(file.word_occurrences, top_n)
    words = list(top_words_dict.keys())
    counts = list(top_words_dict.values())
    
    # Column one will be a bar chart showing word occurrences, simple as.
    ax1.bar(words, counts, edgecolor='black')
    ax1.set_title(f'Top {top_n} Words')
    # Rotates parameters 45 degrees for better visibility
    ax1.tick_params(axis='x', rotation=45)

    # For our 2nd column, use a word length histogram.
    # Get data from TextFile.
    word_lengths_dict = file.word_length_occurrences
    lengths = np.array(list(word_lengths_dict.keys()))
    counts = np.array(list(word_lengths_dict.values()))
    
    # Calculate bins for the histogram.
    # If there are no word lengths (somehow), use a dummy array.
    bins = np.arange(1, lengths.max() + 2) if lengths.size > 0 else np.array([0, 1])

    # Add histogram to figure's 2nd column
    ax2.hist(lengths, bins=bins, weights=counts, edgecolor='black')
    ax2.set_title('Word Length Distribution')
    ax2.set_xlabel('Word Length')
    ax2.set_ylabel('Frequency')

    # Show figure
    plt.tight_layout()
    plt.show(block=True)


def plot_sentence_analysis(file: stex.TextFile, top_n: int = 10) -> None:
    """
    Plots sentence length distribution and the most common sentence lengths.
    Does not return value - shows matplotlib figure.

    Arguments:
        file: TextFile object
    """

    # Same procedure as always. Initialize figure, two columns.
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

    sentence_length_dictionary = file.sentence_length_distribution
    lengths = np.array(list(sentence_length_dictionary.keys()))
    counts = np.array(list(sentence_length_dictionary.values()))
    
    # Calculate bins for the histogram
    samples = np.repeat(lengths, counts)
    bins = np.arange(lengths.min() - 0.5, lengths.max() + 1.5, 1.0)

    # Add histogram to figure's 1st column 
    ax1.hist(lengths, bins=bins, weights=counts, edgecolor='black')
    ax1.set_title('Sentence Length Distribution')
    ax1.set_xlabel('Words per Sentence')
    ax1.set_ylabel('Frequency')

    # We're still relying on the fact that this dictionary is sorted,
    # which it should be from stex_analysis.py. Note that there could
    # be zero sentences, thus the extra check.
    items = list(sentence_length_dictionary.items())
    top_n = min(top_n, len(items))
    top_items = items[:top_n]

    # Jargon, but this pairs elements from the input and produces tuples.
    # (https://stackoverflow.com/questions/12974474/how-to-unzip-a-list-of-tuples-into-individual-lists)
    # top_lengths: all sentence length
    # top_counts: corresponding counts
    top_lengths, top_counts = zip(*top_items) 
    
    # X positions for the columns in our bar chart
    x = np.arange(len(top_lengths))          
    
    # Plot
    ax2.bar(x, top_counts, edgecolor='black')
    ax2.set_xticks(x)
    ax2.set_xticklabels(top_lengths)
    ax2.set_title(f"Top {len(top_lengths)} Most Common Sentence Lengths")
    ax2.set_xlabel("Sentence Length (words)")
    ax2.set_ylabel("Frequency")

    # Show figure
    plt.tight_layout()
    plt.show(block=True)


def plot_character_analysis(file: stex.TextFile, top_n: int=10) -> None:
    """
    Plots the most common characters and a pie chart of character types.
    Does not return a value - shows matplotlib figure.

    Arguments:
        file: TextFile object
        top_n: number of top characters to display
    """

    # You know the drill by now. Initialize figure, two columns
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,5))

    # Top characters. Unconstrained, unlike the stex_pretty version.
    top_chars_dict = file.get_top_elements_of_dictionary(file.character_occurrences, top_n)
    chars = list(top_chars_dict.keys())
    counts = list(top_chars_dict.values())
    ax1.bar(chars, counts, edgecolor='black')
    ax1.set_title(f'Top {top_n} Characters')

    # Pie chart for character types
    letters = file.letter_count
    digits = file.digit_count
    punctuation = file.punctuation_count
    spaces = file.space_count
    other = file.other_count

    pie_labels = ['Letters', 'Digits', 'Punctuation', 'Spaces', 'Other']
    pie_sizes = [letters, digits, punctuation, spaces, other]

    wedges, _, _= ax2.pie(
        pie_sizes,
        autopct='%1.1f%%', # percentages rounded to 1 decimal point
        startangle=90,
        wedgeprops={'edgecolor':'black'},
        pctdistance=1.2    # offsets percentages to be outside of the pie chart
    )

    # Set 2nd columns title, legend, etc.
    ax2.set_title('Character Type Distribution (Extended)')
    ax2.legend(wedges, pie_labels, title='Categories', loc='center left', bbox_to_anchor=(1.2, 0.5))
    ax2.set_aspect('equal') 
    ax2.axis('off')

    # Display figure
    plt.tight_layout()
    plt.show()

def plot_language_confidence(file: stex.TextFile, top_n: int = 5) -> None:
    """
    Plot the top-N language confidence scores as a bar chart.
    Does not return value - shows matplotlib figure.

    Arguments:
        file: TextFile object
        top_n: how many top matches to show (default 5)
    """
    confidences = file.language_probabilities
    
    if not confidences:
        raise ValueError("No confidence scores provided.")

    # Take the top N (or fewer if not enough items)
    # We are, as customary, assuming this dictionary is already sorted
    # by its values.
    items = list(confidences.items())
    top_items = items[:max(1, min(top_n, len(items)))]

    # Separate names and values, convert to percentages
    languages = []
    scores_percentages = []

    for lang, score in top_items:
        languages.append(lang)
        scores_percentages.append(float(score) * 100.0)


    # Plot - only one column in this figure as opposed to other plots.
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(languages, scores_percentages, edgecolor='black') 

    # Annotate each bar with percentage text above it
    for i, bar in enumerate(bars):
        pct = scores_percentages[i]
        x_center = bar.get_x() + bar.get_width() / 2
        y_top = bar.get_height()
        offset = max(1.0, 0.02 * max(scores_percentages))
        ax.text(x_center, y_top + offset, f"{pct:.1f}%", ha='center', va='bottom', fontsize=9)


    # Stylize figure
    ax.set_ylabel("Confidence (%)")
    ax.set_title(f"Top {len(languages)} Language Matches")
    
    # Display figure
    plt.tight_layout()
    plt.show()