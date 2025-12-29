import zipfile
import os
import argparse
import pathlib

from soupsieve import SoupSieve
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

# Opens an epub and returns the path to the extracted contents.
def open_epub(epubpath):
    if not zipfile.is_zipfile(epubpath):
        raise ValueError("The provided file is not a valid epub (zip) file.")
    epub = zipfile.ZipFile(epubpath, 'r')
    epub_extract_path = pathlib.Path.home().joinpath(".epub2txt_temp").joinpath(os.path.splitext(epubpath)[0].split("\\")[-1])
    epub.extractall(epub_extract_path)
    return epub_extract_path

# Handles html parsing and text extraction from epub files.
def extract_text_from_epub(epubpath):
    epub_path = open_epub(epubpath)
    all_text = ""
    for root, dirs, files in os.walk(epub_path):
        if args.verbose:
            print(root + " Contents:")
            print("files:", files)
        for file in files:
            if file.endswith(('.html', '.xhtml', '.htm')):
                file_path = os.path.join(root, file)
                if args.verbose:
                    print(f"Processing file: {file_path}")
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = extraction_handler(file_path)
                    all_text = all_text + text + "\n"
    return all_text

def recurse_div(soup, isVerbose=False):
    for div in soup.find_all('div'):
        for tag in soup.find_all(['b', 'i', 'u', 'em', 'strong', 'a', 'span', 'dl', 'dt', 'dd']):
            tag.unwrap()
        for tag in soup.find_all('div'):
            if isVerbose:
                print("Recursing into div...")
            soup = recurse_div(tag, isVerbose)
    return soup

def extraction_handler(file_path):
    text = ""
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        body = soup.find('body')
        paragraphs = body.descendants
        # WHY WONT YOU WORK
        for tag in soup.find_all(['b', 'i', 'u', 'em', 'strong', 'a', 'span', 'dl', 'dt', 'dd']):
            tag.unwrap()
        
        soup = recurse_div(soup)
        
        for p in paragraphs:
            soup = BeautifulSoup(str(p), 'html.parser')
            # Unwrap formatting tags
            for tag in soup.find_all(['b', 'i', 'u', 'em', 'strong', 'a', 'span', 'dl', 'dt', 'dd']):
                tag.unwrap()
            soup.smooth()
            soup_text = soup.find_all('p', recursive=False)
            for item in soup_text:
                if item.name == 'br':
                    text = text + "\n"
                if item.name == 'p' or item.name == 'div':
                    text = text + p.get_text(separator=" ",strip=True)
                text = text + "\n"
        
        new_text = []
        for line in text.splitlines():
            if line == "\n" or line.strip() == "":
                continue
            stripped_line = line.strip()
            new_text.append(stripped_line)
        return "\n\n".join(new_text)

if __name__ == "__main__":
    # Argument parsing
    argparser = argparse.ArgumentParser(prog="epub2txt", description="Extracts all text from an epub file and (optionally) cleans it up.", usage="epub2txt <epubfile> [-o <outputfile>] [-c]")
    argparser.add_argument("epubfile", help="Path to the epub file to extract text from.")
    argparser.add_argument("-o", "--output", help="Path to the output text file. Defaults to the same name as the epub file with a .txt extension.")
    argparser.add_argument("-c", "--clean", action="store_true", help="Clean up the extracted text. By default off.")
    argparser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output for debugging purposes.")
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
    
    # Open the EPUB file and prepare variables
    print(f"Opening epub file: {epubpath}")
    epub_path = open_epub(epubpath)
    if args.verbose:
        print(f"Extracted epub to temporary path: {epub_path}")
    all_text = ""
    
    # Walk through the extracted epub files and extract text from HTML/XHTML files
    all_text = extract_text_from_epub(epubpath)
    
    # Optionally clean the extracted text
    print("Finished extracting text from epub.")
    if args.clean:
        if args.verbose:
            print("Cleaning up extracted text...")
        all_text = txtcleaner.clean_text(all_text, is_verbose=args.verbose, advanced_cleaning=True)
        if args.verbose:
            print("Text cleanup complete.")
    
    # Finally, write the extracted (and possibly cleaned) text to the output file
    with open(outputpath, 'w', encoding='utf-8') as out_file:
        out_file.write(all_text)
    
    print(f"Extracted text written to: {outputpath}")
    
    print("DONE!")
    print("Beginning cleanup...")
    
    # Cleanup temporary extracted files
    
    # walk the directory tree and remove files and directories
    #for root, dirs, files in os.walk(epub_path, topdown=False):
    #    for name in files:
    #        os.remove(os.path.join(root, name))
    #    for name in dirs:
    #        os.rmdir(os.path.join(root, name))
    #os.rmdir(epub_path)
    print("Cleanup complete.")