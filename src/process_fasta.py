import csv
from pathlib import Path

from src.constants import (
    DB_OUTPUT_FILE,
    DB_OUTPUT_PATH,
    PASTA_INPUT_PATH,
)

db_output_file = DB_OUTPUT_PATH / Path(DB_OUTPUT_FILE)
pasta_input_path = Path(PASTA_INPUT_PATH)


def _write_row_to_db(file, row):
    with file.open("a") as f:
        csv_writer = csv.writer(f, lineterminator="\n")
        csv_writer.writerow(row)


def _create_header(file: Path):
    header = ["id", "seq"]
    _write_row_to_db(file, header)


def _read_file(file):
    with file.open("r") as f:
        lines = f.readlines()
    ids = [line.strip().strip(">") for line in lines if line.startswith(">")]
    seqs = [line.strip() for line in lines if not line.startswith(">")]
    return ids, seqs


def _write_db(ids, seqs, file):
    if not file.exists():
        _create_header(file)
    for id, seq in zip(ids, seqs):
        row = [id, seq]
        _write_row_to_db(file, row)


def process_fasta(file, db_output_file):
    ids, seqs = _read_file(file)
    _write_db(ids, seqs, db_output_file)


def run():
    if pasta_input_path.is_dir():
        for file in pasta_input_path.iterdir():
            process_fasta(file, db_output_file)
        else:
            print(
                f"All files in the `{pasta_input_path.name}` folder were succesfully processed!\n"
            )
    print(f"The CSV {db_output_file.name} was created.")
    return db_output_file


if __name__ == "__main__":
    run()
