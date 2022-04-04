import json
import re
from pathlib import Path
from typing import Dict, Tuple

PATH = Path(r"support_files")

INPUT_FILE = PATH / Path(r"modifiers.html")
OUTPUT_FILE = PATH / Path(r"modifiers.json")

SWISS = PATH / Path(r"swiss_modifiers.html")
FFNCAA = PATH / Path(r"ffncaa_modifiers.html")


def parse_html_modifiers(
    INPUT_FILE: Path,
) -> Tuple[Dict[str, Dict[str, str]], Dict[str, str]]:
    pattern_group = r"select name=\"(\w{3,})\""
    pattern_residue = r"value=\"([A-Z0-9]{3,})\".*>(.+)\s*</"
    pattern_args = r"<input type=\"text\" name=\"(\w{3,})\""

    with INPUT_FILE.open("r") as f:
        contents = f.read()

    lines = contents.replace("><", ">\n<").split("\n")

    output_dict: Dict[str, Dict[str, str]] = {}
    args_dict: Dict[str, str] = {}

    for line in lines:
        matches_group = re.search(pattern_group, line)
        matches_residues = re.search(pattern_residue, line)
        matches_args = re.search(pattern_args, line)
        if matches_group:
            current_group = matches_group.groups()[0]
            output_dict[current_group] = {}
        elif matches_residues:
            modifier_code, modifier_str = matches_residues.groups()
            output_dict[current_group][modifier_str] = modifier_code
        elif matches_args:
            args_dict[current_group] = matches_args.groups()[0]
        else:
            continue
    return output_dict, args_dict


def get_group(aminoacid: str, library: Dict[str, Dict[str, str]]) -> str:
    for key in library:
        if aminoacid in library[key]:
            return key
        else:
            continue
    else:
        return ""


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


swiss, swiss_args = parse_html_modifiers(SWISS)
ffncaa, ffncaa_args = parse_html_modifiers(FFNCAA)

if __name__ == "__main__":
    main()
