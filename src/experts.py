from re import S
from typing import Dict, List, Tuple

from src.modifiers_parser import get_group
from src.settings import MODIFICATIONS_RULES
from src.constants import swiss, swiss_args, ffncaa, ffncaa_args
from src.settings import SETTINGS, LIBRARY


def _return_indexes(sequence: str, letter: str) -> List[str]:
    """Return list of indices of a given letter on a sequence."""
    return [str(i + 1) for i, c in enumerate(sequence) if c == letter]


def _get_my_dict(sequence: str) -> Dict[str, str]:
    libraries = ["swiss", "ffncaa"]
    my_dict = {}
    for letter in MODIFICATIONS_RULES:
        aminoacid = MODIFICATIONS_RULES[letter]
        for library in libraries:
            lib_dict = globals()[library]
            group = get_group(aminoacid, lib_dict)
            if group:
                my_dict[group] = lib_dict[group][aminoacid]
                argument = globals()[f"{library}_args"][group]
                my_dict[argument] = ",".join(_return_indexes(sequence, letter))
    return my_dict


def _get_key(val, dictionary):
    for key, value in dictionary.items():
        if val == value:
            return key


def _get_mods_expert(sequence: str) -> List[str]:
    my_dict = _get_my_dict(sequence)
    mods = ["No modification" for _ in range(len(sequence))]
    for key in my_dict:
        if key in ffncaa:
            modification = _get_key(my_dict[key], ffncaa[key])
            for index in my_dict[ffncaa_args[key]].split(","):
                mods[int(index) - 1] = modification
        elif key in swiss:
            modification = _get_key(my_dict[key], swiss[key])
            for index in my_dict[swiss_args[key]].split(","):
                mods[int(index) - 1] = modification
    return mods


def generate_params(sequence: str) -> Tuple[Dict[str, str], List[str]]:
    SETTINGS["MAX_FILE_SIZE"] = "1000000"
    SETTINGS["seq"] = sequence
    SETTINGS["ffncaa"] = LIBRARY
    SETTINGS["send"] = "Submit sequence for prediction"
    my_dict = _get_my_dict(sequence)
    return (
        {
            **SETTINGS,
            **{key: list(swiss[key].values())[0] for key in swiss},
            **{key: list(ffncaa[key].values())[0] for key in ffncaa},
            **dict.fromkeys(swiss_args.values(), ""),
            **dict.fromkeys(ffncaa_args.values(), ""),
            **my_dict,
        },
        _get_mods_expert(sequence),
    )
