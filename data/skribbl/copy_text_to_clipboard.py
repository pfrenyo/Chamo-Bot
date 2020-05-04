import argparse
import pyperclip
from os.path import dirname, join

SKRIBBL = True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="name of the file whose content you will copy to clipboard")
    args = parser.parse_args()
    filepath = join(dirname(__file__), args.filename)
    with open(filepath, "r", encoding='utf-8') as f:
        txt = f.read()
        if SKRIBBL:
            txt += "\n\n\n\n"
        pyperclip.copy(txt)
