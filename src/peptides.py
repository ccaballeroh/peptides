import csv
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from src.constants import (
    BASE_URL,
    CONVERSION,
    DOWNLOAD_PATH,
    LETTERS_FIELDS,
    LOG_FILE,
    MODIFICATIONS_FIELDS,
    MODIFICATIONS_RULES,
    SETTINGS,
)

__all__ = ["send_sequence", "download", "send_sequence_mods"]


DOWNLOAD_PATH_ = Path(DOWNLOAD_PATH)
LOG_FILE_ = Path(LOG_FILE)

# Auxiliar functions


def _get_ran_url(sequence: str) -> str:
    """Get ran_id for a given sequence."""

    url = BASE_URL + "mod_ds_upload.php"
    fields = {
        "MAX_FILE_SIZE": 1000000,
        "seq": sequence,
        "fflib": "ffncaa",
        "send": "Submit and Go to Next Step",
    }
    request = requests.post(url, data=fields)
    soup = BeautifulSoup(request.text, "html.parser")
    action = soup.find("form", attrs={"name": "form1"}).get("action")
    return action


def _call_form(ran_url: str, fields: Dict[str, str]) -> None:
    """Make a call for a given ran_id and data fields."""

    url = BASE_URL + ran_url
    request = requests.post(url, data=fields)
    if request.text.find("Your sequence has been submitted") == -1:
        print("Process failed")
        exit(-1)


def _generate_letters(sequence: str) -> Dict[str, str]:
    """Generate parameter values for each letter in sequence."""

    return {
        key: value
        for key, value in zip(LETTERS_FIELDS, [letter for letter in sequence])
    }


def _generate_modifications(mods_list: List[str]) -> Dict[str, str]:
    """Generate parameter values for the modifications."""

    return {key: value for key, value in zip(MODIFICATIONS_FIELDS, mods_list)}


def _generate_fields(sequence: str, modifications: List[str]) -> Dict[str, str]:
    """Generate one dictionary of parameters to make the request."""

    return {
        **_generate_letters(sequence),
        **_generate_modifications(modifications),
        **SETTINGS,
    }


def _give_mods(sequence: str) -> List[str]:
    """Generate list of predefined modifications for each letter in sequence."""

    return [
        MODIFICATIONS_RULES[letter]
        if letter in MODIFICATIONS_RULES
        else "No Modification"
        for letter in sequence
    ]


def _parse_modifications_list(modifications: List[str]) -> List[str]:
    """Parse each modification to the value accepted by the webpage."""

    return [CONVERSION[mod] for mod in modifications]


def _logging(sequence: str, modifications: List[str], ran_id: str) -> None:
    """Log each sequence, modifications, and ran id."""

    if not LOG_FILE_.exists():
        with LOG_FILE_.open("w") as file:
            header = ["sequence", *[f"mod{i}" for i in range(1, 26)], "ran_id"]
            csv_writer = csv.writer(file, lineterminator="\n")
            csv_writer.writerow(header)
    with LOG_FILE_.open("a") as file:
        row = [sequence, *modifications, ran_id]
        csv_writer = csv.writer(file, lineterminator="\n")
        csv_writer.writerow(row)


# Module's main functions


def send_sequence_mods(
    sequence: str, mods_raw: List[str], download_flag: bool = False
) -> None:
    """Send a sequence along with a modification list."""

    modifications = _parse_modifications_list(mods_raw)
    fields = _generate_fields(sequence, modifications)
    ran_url = _get_ran_url(sequence)
    _call_form(ran_url, fields)
    ran_id = ran_url.split("=")[1]
    _logging(sequence, mods_raw, ran_id)
    if download_flag:
        download(ran_id)


def send_sequence(sequence: str, download_flag: bool = False) -> None:
    """Send a sequence with a preset list of modifications for each letter."""

    mods = _give_mods(sequence)  # assigns predefined modifications
    send_sequence_mods(sequence, mods, download_flag=download_flag)


def download(ran_id: str, waiting_time: int = 60) -> None:
    """Download a results file given a ran_id."""

    if not DOWNLOAD_PATH_.exists():
        DOWNLOAD_PATH_.mkdir()
    url = f"https://webs.iiitd.edu.in/tmp/pepstrmod/pep_{ran_id}/pepstr{ran_id}.pdb"
    filename = f"{ran_id}.pdb"
    completed = False
    while not completed:
        try:
            urllib.request.urlretrieve(url, DOWNLOAD_PATH_ / filename)
            completed = True
        except urllib.error.HTTPError:
            print(f"Try again in {waiting_time/60} mins.")
            time.sleep(waiting_time)
    print(f"{filename} successfully downloaded")
