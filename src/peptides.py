import time
import urllib.error
import urllib.request
from pathlib import Path

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


def _get_ran_url(sequence):
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


def _call_form(ran_url, fields):
    url = BASE_URL + ran_url
    request = requests.post(url, data=fields)
    if request.text.find("Your sequence has been submitted") == -1:
        print("Process failed")
        exit(-1)


def _generate_letters(test_seq):
    return {
        key: value
        for key, value in zip(LETTERS_FIELDS, [letter for letter in test_seq])
    }


def _generate_modifications(mods_list):
    return {key: value for key, value in zip(MODIFICATIONS_FIELDS, mods_list)}


def _generate_fields(sequence, modifications):
    return {
        **_generate_letters(sequence),
        **_generate_modifications(modifications),
        **SETTINGS,
    }


def _give_mods(sequence):
    return [
        MODIFICATIONS_RULES[letter]
        if letter in MODIFICATIONS_RULES
        else "No Modification"
        for letter in sequence
    ]


def _parse_modifications_list(modifications):
    return [CONVERSION[mod] for mod in modifications]


def _logging(sequence, modifications, ran_id):
    if not LOG_FILE_.exists():
        with LOG_FILE_.open("w") as file:
            print(
                "sequence",
                *[f"mod{i}" for i in range(1, 26)],
                "ran_id",
                sep=",",
                file=file,
            )
    with LOG_FILE_.open("a") as file:
        print(sequence, *modifications, ran_id, sep=",", file=file)


def send_sequence_mods(sequence, modifications_raw, download_flag=False):
    modifications = _parse_modifications_list(modifications_raw)
    fields = _generate_fields(sequence, modifications)
    ran_url = _get_ran_url(sequence)
    _call_form(ran_url, fields)
    ran_id = ran_url.split("=")[1]
    _logging(sequence, modifications_raw, ran_id)
    if download_flag:
        download(ran_id)


def send_sequence(sequence, download_flag=False):
    mods = _give_mods(sequence)
    send_sequence_mods(sequence, mods, download_flag=download_flag)


def download(ran_id, waiting_time=60):
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
