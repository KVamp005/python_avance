from pathlib import Path
import pandas as pd

# chemins
DATA_PATH = Path("data.csv")
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "cleanpro_data.csv"

# 1) Lecture du CSV (on saute les lignes cassées)
df = pd.read_csv(
    DATA_PATH,
    sep=";",
    dtype=str,                # tout en texte au début
    encoding="utf-8",
    keep_default_na=False,
    on_bad_lines="skip"
)

# 2) Renommer les colonnes (propre, simple)
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# 3) Gérer les valeurs manquantes / bizarres
missing_tokens = [
    "", "None", "none",
    "Nan", "nan",
    "N/A", "n/a",
    "NA", "na",
    "---"
]
df = df.replace({token: None for token in missing_tokens})

# 4) Conversion des types de base

# id_client -> entier nullable
if "id_client" in df.columns:
    df["id_client"] = pd.to_numeric(df["id_client"], errors="coerce").astype("Int64")

# age -> entier nullable
if "age" in df.columns:
    df["age"] = pd.to_numeric(df["age"], errors="coerce").astype("Int64")

# dates -> datetime (on laisse pandas gérer les formats, on force juste dayfirst)
for col in ["date_inscription", "derniere_connexion"]:
    if col in df.columns:
        df[col] = pd.to_datetime(
            df[col],
            errors="coerce",
            dayfirst=True
        )

# montant_total_eur -> float
if "montant_total_eur" in df.columns:
    montant = df["montant_total_eur"].astype(str).str.strip()

    # enlever signes et espaces chelous
    montant = montant.str.replace("€", "", regex=False)
    montant = montant.str.replace("\u00a0", "", regex=False)  # espace insécable
    montant = montant.str.replace(" ", "", regex=False)

    # remplacer virgule par point (format FR)
    montant = montant.str.replace(",", ".", regex=False)

    df["montant_total_eur"] = pd.to_numeric(montant, errors="coerce")

# 5) Normalisation des booléens (actif, newsletter_ok)
bool_mapping = {
    "oui": True,
    "yes": True,
    "true": True,
    "1": True,
    "non": False,
    "no": False,
    "false": False,
    "0": False,
}

if "actif" in df.columns:
    col = df["actif"].astype(str).str.strip().str.lower()
    df["actif"] = col.map(bool_mapping)
    df["actif"] = df["actif"].astype("boolean")

if "newsletter_ok" in df.columns:
    col = df["newsletter_ok"].astype(str).str.strip().str.lower()
    df["newsletter_ok"] = col.map(bool_mapping)
    df["newsletter_ok"] = df["newsletter_ok"].astype("boolean")
    # par défaut, pas abonné si vide ou valeur chelou
    df["newsletter_ok"] = df["newsletter_ok"].fillna(False)

# 6) supprimer les lignes complètement vides
df = df.dropna(how="all")

# 7) Sauvegarde
OUTPUT_DIR.mkdir(exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False, sep=";")

print("Aperçu :")
print(df.head())
print("\nTypes :")
print(df.dtypes)
print(f"\nFichier nettoyé enregistré dans : {OUTPUT_FILE}")
