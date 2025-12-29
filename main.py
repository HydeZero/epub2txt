import zipfile
import os
import argparse
import pathlib
try:
    import txtcleaner
except ImportError:
    print("""Error: txtcleaner module not found.
This is most likely an issue with compilation if you are using an executable.
Otherwise, try deleting and redownloading the repository.
Please ensure txtcleaner.py is in the same directory as this script.""")
    exit(1)
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("""Error: BeautifulSoup4 is required to run this script. Please install it using 'pip install beautifulsoup4'.
          
It is highly recommended to install it in a virtual environment to avoid breaking other projects.
If you are NOT in a virtual environment already, use these commands (no sudo or privelage is needed):
    > python -m venv .venv --prompt epub2txt
    > source .venv/bin/activate  # On Linux
    > .venv\\Scripts\\Activate.ps1 # On Windows PowerShell
    > .venv\\Scripts\\activate.bat # On Windows CMD
    > pip install beautifulsoup4
    
If this message is showing up on an executable, something went wrong when building and we will need a new executable.""")
    exit(1)
try:
    from markdownify import MarkdownConverter
    import strip_markdown
except ImportError:
    print("""Error: markdownify and strip_markdown are required to run this script. Please install them using 'pip install markdownify strip-markdown'.
          
It is highly recommended to install it in a virtual environment to avoid breaking other projects.
If you are NOT in a virtual environment already, use these commands (no sudo or privelage is needed):
    > python -m venv .venv --prompt epub2txt
    > source .venv/bin/activate  # On Linux
    > .venv\\Scripts\\Activate.ps1 # On Windows PowerShell
    > .venv\\Scripts\\activate.bat # On Windows CMD
    > pip install markdownify strip-markdown
    
If this message is showing up on an executable, something went wrong when building and we will need a new executable.""")
    exit(1)

# Opens an epub and returns the path to the extracted contents.
def open_epub(epubpath):
    # Check if the file is a valid zip (epub) file.
    if not zipfile.is_zipfile(epubpath):
        raise ValueError("The provided file is not a valid epub (zip) file.")
    # Extract the epub contents to a temporary directory.
    epub = zipfile.ZipFile(epubpath, 'r')
    epub_extract_path = pathlib.Path.home().joinpath(".epub2txt_temp").joinpath(os.path.splitext(epubpath)[0].split("\\")[-1])
    epub.extractall(epub_extract_path)
    # Finally, return the path to the extracted contents.
    return epub_extract_path

# Handles html parsing and text extraction from epub files.
def extract_text_from_epub(epubpath):
    # Open the epub file and get the extracted path.
    epub_path = open_epub(epubpath)
    all_text = ""
    # Begin a directory walk to find all of the html/xhtml files.
    for root, dirs, files in os.walk(epub_path):
        if args.verbose:
            print(root + " Contents:")
            print("files:", files)
        for file in files:
            # If we find an html, xhtml, or htm file, process it.
            if file.endswith(('.html', '.xhtml', '.htm')):
                file_path = os.path.join(root, file)
                if args.verbose:
                    print(f"Processing file: {file_path}")
                text = extraction_handler(file_path)
                # Add a chapter splitter for readability.
                all_text = all_text + text + "\n\n\n\n----------------\n\n\n\n"
    return all_text

# Convert BeautifulSoup object to markdown text.
# This is the default recommended function in the markdownify pip page.
def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


def extraction_handler(file_path):
    text = ""
    with open(file_path, 'r', encoding='utf-8') as f:
        # Make the BeautifulSoup object from the file.        
        soup = BeautifulSoup(f, 'html.parser')
        # Extract the body content.
        body = soup.find('body')
        # Convert the body to markdown text.
        text = md(body)
        # Finally, remove the markdown formatting to get plain text.
        text = strip_markdown.strip_markdown(text)
        
        # Now remove excessive new lines
        new_text = []
        for line in text.splitlines():
            # If the line is empty or only whitespace, skip it.
            if line == "\n" or line.strip() == "":
                continue
            # Otherwise, strip the line and add it to the new text list.
            stripped_line = line.strip()
            new_text.append(stripped_line)
        # Collapse the new text list back into a single string with double new lines.
        return "\n\n".join(new_text)

if __name__ == "__main__":
    # Argument parsing
    argparser = argparse.ArgumentParser(prog="epub2txt", description="Extracts all text from an epub file and (optionally) cleans it up.", usage="epub2txt <epubfile> [-o <outputfile>] [-c]")
    argparser.add_argument("epubfile", help="Path to the epub file to extract text from.")
    argparser.add_argument("-o", "--output", help="Path to the output text file. Defaults to the same name as the epub file with a .txt extension.")
    argparser.add_argument("-c", "--clean", action="store_true", help="Clean up the extracted text. By default off.")
    argparser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output for debugging purposes.")
    
    # Try to parse arguments and handle errors.
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
    
    # Extract text from the epub
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
    
    # walk the directory tree and remove files and directories.
    # For every file in the tree bottom-up, remove the file, then remove the directory if empty.
    for root, dirs, files in os.walk(epub_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    # Finally, remove the main extracted epub directory.
    os.rmdir(epub_path)
    print("Cleanup complete.")