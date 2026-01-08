from pathlib import Path
import pandas as pd

DATA_PATH = Path("data.csv")
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "clean_data.csv"

# Lecture du CSV
df = pd.read_csv(
    DATA_PATH,
    sep=";",
    dtype=str,
    encoding="utf-8",
    keep_default_na=False,
    on_bad_lines="skip"  # IMPORTANT pour éviter l'erreur de la ligne 23
)

# Nettoyages courants
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

df = df.replace({
    "": None,
    "None": None,
    "Nan": None, "nan": None,
    "N/A": None, "n/a": None,
    "NA": None, "na": None
})

df = df.replace({
    "true": True,
    "false": False,
    "oui": True,
    "non": False
})

# conversions de types
df["id_client"] = pd.to_numeric(df["id_client"], errors="coerce").astype("Int64")
df["age"] = pd.to_numeric(df["age"], errors="coerce").astype("Int64")

df["date_inscription"] = pd.to_datetime(
    df["date_inscription"],
    errors="coerce",
    format="%Y-%m-%d"  # car 2024-03-11 = année-mois-jour
)


df["derniere_connexion"] = pd.to_datetime(
    df["derniere_connexion"],
    errors="coerce",
    format="%Y-%m-%d"
)

montant = df["montant_total_eur"].str.replace(" ", "", regex=False)
montant = montant.str.replace(",", ".", regex=False)
df["montant_total_eur"] = pd.to_numeric(montant, errors="coerce")

df["newsletter_ok"] = df["newsletter_ok"].fillna(False)

# supprimer les lignes complètement vides
df = df.dropna(how="all")

# créer le dossier output si besoin
OUTPUT_DIR.mkdir(exist_ok=True)

print(df.head())

# sauvegarde
df.to_csv(OUTPUT_FILE, index=False)
print(f"Fichier nettoyé enregistré dans : {OUTPUT_FILE}")
