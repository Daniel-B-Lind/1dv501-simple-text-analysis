# 1DV501-Final

Simple Text Analyser (STEX) written for the final project of 1DV501.

Components:
- stex_main.py - handles TUI and user prompts
- stex_analysis.py - ingests text files 
- stex_filing.py - stores analysis results in TextFile objects
- stex_pretty.py - generates printable representations of data
- stex_json.py - serializes/deserializes data
- stex_plotting.py - visualizes data using matplotlib
    
Auxiliary:
- trigram_sample_generator.py - generates standalone JSON files containing word boundary trigram frequency for provided texts

The language detection feature is extensible. Built-in support for Danish, English, French, German, Hungarian, Italian, and Swedish.
To add support for more languages, get a sizeable text file written in your language of choice and run
`trigram_sample_generator.py textfile.txt lang_sample_{Name_of_Language}.json`
Drop the resulting .json file into the resources folder. The engine will automatically detect the file so long as it's correctly named
and contains valid json.
