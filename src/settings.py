## Simulation settings

SETTINGS = {
    "email": "myemail@email.com",
    "time": "50ps",  # 50 picoseconds
    "env": "vac",  # Peptide env: vaccumm
    "topol": "no",
    "cluster": "no",
    "traj": "no",
    "graph": "no",  # Graph and RMS: No
}

## File names and folder paths

LOG_FILE = "log.csv"  # name of log file to store sequence, modifications and sim ran_id
DB_OUTPUT_FILE = "db.csv"  # name of fasta processed files
PASTA_INPUT_PATH = "inputs"  # name of folder where all pasta files are located
DOWNLOAD_PATH = "outputs"  # name of folder where to download simulations results

## Modification rules

MODIFICATIONS_RULES = {
    "V": "norvaline",
    "L": "norleucine",
    "I": "2aminobutyricacid",
    "R": "No Modification",  #  It's supposed to be 2,4-diaminobutyric acid, but it's not in the options
}

