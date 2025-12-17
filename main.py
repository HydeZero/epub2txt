import zipfile
import os
import argparse
import txtcleaner
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("""Error: BeautifulSoup4 is required to run this script. Please install it using 'pip install beautifulsoup4'.
          
It is highly recommended to install it in a virtual environment to avoid breaking other projects.
Use these commands (no sudo or privelage is needed):
    > python -m venv .venv --prompt epub2txt
    > source .venv/bin/activate  # On Linux
    > .venv\\Scripts\\Activate.ps1 # On Windows PowerShell
    > .venv\\Scripts\\activate.bat # On Windows CMD
    > pip install beautifulsoup4
    
If this message is showing up on an executable, something went wrong when building and we will need a new executable.""")
    exit(1)

if __name__ == "__main__":
    
    # Argument parsing
    argparser = argparse.ArgumentParser(prog="epub2txt", description="Extracts all text from an epub file and (optionally) cleans it up.", usage="epub2txt <epubfile> [-o <outputfile>] [-c]")
    argparser.add_argument("epubfile", help="Path to the epub file to extract text from.")
    argparser.add_argument("-o", "--output", help="Path to the output text file. Defaults to the same name as the epub file with a .txt extension.")
    argparser.add_argument("-c", "--clean", action="store_true", help="Clean up the extracted text. By default off.")
    try:
        args = argparser.parse_args()
    except Exception as e:
        print("Error parsing arguments:", e)
        argparser.print_help()
        exit(1)
    # Determine output file path
    epubpath = args.epubfile
    if args.output:
        outputpath = args.output
    else:
        outputpath = os.path.splitext(epubpath)[0] + ".txt"