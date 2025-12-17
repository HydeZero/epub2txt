import zipfile
import os
import argparse

argparser = argparse.ArgumentParser(prog="epub2txt", description="Extracts all text from an epub file and (optionally) cleans it up.")