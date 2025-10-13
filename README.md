# 1DV501-Final

This year, the project will be the same for everyone
• The basis of the project is to take a “large” text mass and analys its text
‣ A large text means a sizable book
• Doing so, you will cover several important aspects of Python programming:
‣ I/O in an efficient way
‣ Data structures like lists, sets and dictionaries
‣ Working with user input
‣ Displaying data visually using Matplotlib

The project will be described in full first, but for different grades some of the parts can be omitted
• The program will have a text based user interface with different menu options
• A file, selected by the user, must be loadable from a list of possible files
‣ This is the file to be analysed
• Create statistics from the file
• Visualise the statistics
• Save a file to disk containing the statistics

Statistics
• The following statistics are to be handled:
‣ Basic statistics (number of lines, words, characters; average words per line, characters per word) 
‣ Word analysis (top 10 words, word length distribution, unique words, words only appearing once)
‣ Sentence analysis (average words per sentence, longest and shortest, sentence distribution)
‣ Character analysis (letter frequency distribution, punctuation statistics, case distribution)

• All visualisation will be done using Matplotlib
• For each analysis, you will show graphs for the statistics
‣ Where suitable
‣ For example:
– Basic statistics: bar chart of text composition and pie chart of character types
– Word analysis: bar chart of most common words and histogram of word lengths
• Show several (suitable) graph types (bar chart, histogram, pie chart and so on)
• Make sure that labels are easy to read (that is, not overlapping)

• As memory is limited on Jupyter, it is important that you never load the entire file into memory
• Let’s restate that:
**Do not load the entire file into memory**
• Use several of the built-in data structures
‣ Dictionaries for counting words
‣ Lists for lengths
‣ Sets for unique words

Code Quality
• This is the first part that you will submit for review
• The code quality is therefore very important and can be the reason for a higher or lower grade
• Remember:
‣ Use functions to break down the problem into manageable pieces
‣ Pass data between functions using parameters and return values, that is, do not use global variables
‣ Each function should have a single, clear responsibility
‣ Separate data processing from visualisation
‣ Keep the main programme loop clean and readable
• Suitable comments are part of good code quality

Text File
• To show that your program works, you will need to use it on a large text, preferably a book
• The size of the book must be larger than one megabyte
• You will find many really large books on Project Gutenberg and we recommend that you use one of those
‣ Try to find something that not “everyone else” is using
• For Swedish speaking students, the site Project Runeberg can be used instead
‣ For other languages, there should be similar services and you may use any of those if you like
• Important: when developing your program, use a smaller file to make the program quicker and easier to debug

Requirements for All Grades
• For the grade E and above, the following needs to be done:
‣ Have a menu with options
‣ List all text files in the current directory
‣ Process a selected file
‣ Show basic statistics like number of lines, words and characters
‣ Show the statistics using Matplotlib
• Code quality and structure will affect the grade in a positive or negative way

Requirements for Grade C
• All of the previous ones, but also:
‣ Additional statistics, at least one of “word”, “sentence” and “character”
‣ Visualise these using Matplotlib
‣ Have the possibility to export the statistics
• The file format for the export is up to you, but it should be easy for a human to read
‣ It can be a simple textfile or something like JSON or XML

Requirements for Grade B
• All of the previous ones, but also:
‣ Error handling for all input
‣ All of the different statistics
‣ Visualisation for all the statistics
‣ All of the statistics exported in the summary

Requirements for Grade A
• Of course, all of the above, but also:
*Something that will amaze us 😂*
• This could be additional functionality like:
‣ Readability scores (Flesch or Lix)
‣ Comparative analysis between text files
‣ N-gram analysis (find common 2-word or 3-word phrases)
• But it could also be something else, that we have not thought of at all
‣ It must, however, be fairly simple for us to run