from pathlib import Path
from datetime import datetime
import shutil

RAW_DIR = Path("raw_logs")
ARCHIVE_DIR = Path("archive")
OUTPUT_DIR = Path("output")

# créer les dossiers s'ils n'existent pas
OUTPUT_DIR.mkdir(exist_ok=True)
ARCHIVE_DIR.mkdir(exist_ok=True)

# nom du fichier daté
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
OUTPUT_FILE = OUTPUT_DIR / f"errors_{timestamp}.log"

errors = []

# parcourir tous les .log
for log_file in RAW_DIR.glob("*.log"):
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line:
                errors.append(f"[{log_file.name}] {line.strip()}")

    # déplacer le log dans archive/
    shutil.move(str(log_file), ARCHIVE_DIR / log_file.name)

# écrire les erreurs
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for line in errors:
        f.write(line + "\n")

print(f"Extraction terminée : {len(errors)} erreurs trouvées.")
print(f"Fichier généré : {OUTPUT_FILE}")
print("Logs archivés dans :", ARCHIVE_DIR)
