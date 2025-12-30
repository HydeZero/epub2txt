# epub2txt
### Converts unencrypted, DRM-free EPUB files to text files


> [!IMPORTANT]
> You will have to make a virtual environment to run the code. If you can't, use the [compiled tools.](https://github.com/HydeZero/epub2txt/releases/latest)

> [!NOTE]
> Antivirus software may flag the executable. This is due to the executable not being used often and the fact that it is a one-file compilation with PyInstaller. This is common, see [this PyInstaller issue](https://github.com/pyinstaller/pyinstaller/issues/6754) and [this Python discussion](https://discuss.python.org/t/pyinstaller-false-positive/43171) for more info.
> THIS DOES NOT IMPACT THE REGULAR PYTHON FILE.

## USAGE

Make a virtual environment with `python3 -m venv .venv --prompt epub2txt`. Then activate the environment with `.venv\Scripts\Activate.ps1` for Windows PowerShell, `.venv\Scripts\activate.bat` for Windows CMD, or `source .venv/bin/activate` for Linux.

Here is the help output for reference:

```
usage: epub2txt <epubfile> [-o <outputfile>] [-c] [-a] [-k] [-v] [-l <list_to_keep>]

Extracts all text from an epub file and (optionally) cleans it up.

positional arguments:
  epubfile              Path to the epub file to extract text from.

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT   Path to the output text file. Defaults to the same name as the epub file with a .txt extension.
  -c, --clean           Clean up the extracted text. By default off.
  -v, --verbose         Enable verbose output for debugging purposes.
  -a, --advanced-cleaning Enable advanced cleaning mode in text cleaner, removing everything outside of the Basic Latin range. Only works if the --clean flag is set.
  -k, --keep-accents    Keep accented characters during cleaning. Only works if the --clean flag is set.
  -l, --list-to-keep [LIST_TO_KEEP ...] List of characters to keep during cleaning, even if they are not in the acceptable utf-8 characters list. Only works if the --clean flag is set. Supply as a space-separated list of characters without quotes or brackets surrounding them.
```

### EXAMPLE USAGE:
```bash
epub2txt example_ebook.epub -o example_ebook_2_txt.txt -c

Opening epub file: /home/user/example_ebook.epub
Finished extracting text from epub.
Extracted text written to /home/user/example_ebook_2_txt.txt
DONE!
Begining cleanup...
Cleanup complete.
```

## What does cleanup do?

Cleanup mode runs the extracted text through txtcleaner.py, another python file in this repository. It basically replaces characters that may not show up on all devices (i.e. smart quotes, elipses, em dashes...) with their equivalents (i.e. smart quotes becoming `"` or `'`, elipeses becoming `...`, and em dashes becoming `-`). It also tries to remove all characters outside the Basic Latin block of Unicode (`0000` through `007F`, aka ordinals 0 through 127.)

This also impacts accented characters, like À, æ, and ñ. Replacements will be implemented or I might decide to allow you to change the range from Basic Latin to Latin Extended-B.