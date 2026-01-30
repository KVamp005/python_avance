from pathlib import Path
import pandas as pd

# chemins
DATA_PATH = Path("data.csv")
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "clean_data.csv"

# 1) lecture du CSV brut
df = pd.read_csv(
    DATA_PATH,
    sep=";",
    dtype=str,                # tout en texte au début
    encoding="utf-8",
    keep_default_na=False,
    on_bad_lines="skip"       # ignore les lignes cassées
)

# 2) renommer les colonnes (en snake_case simple)
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# 3) gestion basique des valeurs manquantes (vides, variantes de NA)
df = df.replace({
    "": None,
    "None": None,
    "Nan": None, "nan": None,
    "N/A": None, "n/a": None,
    "NA": None, "na": None
})

# 4) normalisation booléens simples
df = df.replace({
    "true": True,
    "false": False,
    "oui": True,
    "non": False
})

# 5) conversions de types simples (si les colonnes existent)

# id_client -> entier
if "id_client" in df.columns:
    df["id_client"] = pd.to_numeric(df["id_client"], errors="coerce").astype("Int64")

# age -> entier
if "age" in df.columns:
    df["age"] = pd.to_numeric(df["age"], errors="coerce").astype("Int64")

# date_inscription -> date
if "date_inscription" in df.columns:
    df["date_inscription"] = pd.to_datetime(
        df["date_inscription"],
        errors="coerce",
        dayfirst=True  # format jour/mois/année
    )

# derniere_connexion -> date
if "derniere_connexion" in df.columns:
    df["derniere_connexion"] = pd.to_datetime(
        df["derniere_connexion"],
        errors="coerce",
        dayfirst=True
    )

# montant_total_eur -> float (en remplaçant virgule par point)
if "montant_total_eur" in df.columns:
    montant = df["montant_total_eur"].str.replace(" ", "", regex=False)
    montant = montant.str.replace(",", ".", regex=False)
    df["montant_total_eur"] = pd.to_numeric(montant, errors="coerce")

# 6) gestion simple des valeurs manquantes après conversion
#    - supprimer lignes totalement vides
df = df.dropna(how="all")

# exemple : si newsletter_ok existe, on peut remplir les vides par False
if "newsletter_ok" in df.columns:
    df["newsletter_ok"] = df["newsletter_ok"].fillna(False)

# 7) création du dossier et export
OUTPUT_DIR.mkdir(exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False, sep=";")

print("OK, fichier nettoyé enregistré dans :", OUTPUT_FILE)
print(df.head())
