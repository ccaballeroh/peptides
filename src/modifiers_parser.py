import json
import re
from pathlib import Path

PATH = Path(r"support_files")
INPUT_FILE = PATH/Path(r"modifiers.html")
OUTPUT_FILE = PATH/Path(r"modifiers.json")

def main():
    pattern = r"value=\"(.+)\">(.+)<"

    with INPUT_FILE.open("r") as f:
        contents = f.readline()

    lines = contents.replace("><", ">\n<").split("\n")

    my_dict = {}

    for line in lines:
        matches = re.search(pattern, line)
        if matches:
            modifier_code, modifier_str = matches.groups()
            my_dict[modifier_str] = modifier_code

    with OUTPUT_FILE.open("w") as f:
        json.dump(my_dict, f)




if __name__ == "__main__":
    main()