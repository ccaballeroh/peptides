import json
from pathlib import Path

from src import modifiers_parser
from src.settings import (
    SETTINGS,
    DB_OUTPUT_FILE,
    PASTA_INPUT_PATH,
    LOG_FILE,
    DOWNLOAD_PATH,
    MODIFICATIONS_RULES,
)

__all__ = [
    "BASE_URL",
    "DOWNLOAD_PATH",
    "LOG_FILE",
    "LETTERS_FIELDS",
    "MODIFICATIONS_FIELDS",
    "SETTINGS",
    "CONVERSION",
    "DB_OUTPUT_FILE",
    "PASTA_INPUT_PATH",
    "MODIFICATIONS_RULES",
]

BASE_URL = "https://webs.iiitd.edu.in/raghava/pepstrmod/"
LETTERS_FIELDS = [f"aa{i}" for i in range(1, 26)]
MODIFICATIONS_FIELDS = [f"secstr{i}" for i in range(1, 26)]
_MODIFIERS_FILE = Path(r"support_files/modifiers.json")

if not _MODIFIERS_FILE.exists():
    modifiers_parser.main()

with _MODIFIERS_FILE.open("r") as f:
    CONVERSION = json.load(f)

DB_OUTPUT_PATH = Path(r".")
