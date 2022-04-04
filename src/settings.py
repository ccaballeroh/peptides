## Simulation settings

SETTINGS = {
    "email": "myemail@email.com",
    "time": "50ps",  # 50 picoseconds other option is 100ps
    "env": "vac",  # Peptide env: vaccumm
    "topol": "no",
    "cluster": "no",
    "traj": "no",
    "graph": "no",  # Graph and RMS: No
}

LIBRARY = "ffncaa"  # other option is "swiss"

## File names and folder paths

LOG_FILE = "log.csv"  # name of log file to store sequence, modifications and sim ran_id
DB_OUTPUT_FILE = "db.csv"  # name of fasta processed files
FASTA_INPUT_PATH = "inputs"  # name of folder where all fasta files are located
DOWNLOAD_PATH = "outputs"  # name of folder where to download simulations results

## Modification rules

MODIFICATIONS_RULES = {
    "V": "norvaline",
    "L": "norleucine",
    "I": "2-aminobutyric acid",  # This is incompatible with the following because both are on the same group
    "R": "diaminobutyric acid",
}

