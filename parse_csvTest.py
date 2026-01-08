from pathlib import Path
import pandas as pd

# chemins des fichiers
DATA_PATH = Path("data.csv")
OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "clean_data.csv"


def load_raw_csv(path: Path) -> pd.DataFrame:
    """Lecture brute du CSV en mode 'tout en texte'."""
    df = pd.read_csv(
        path,
        sep=";",                  # séparateur ;
        encoding="utf-8",
        dtype=str,                # tout en string au début
        keep_default_na=False,    # évite les NaN automatiques
        on_bad_lines="skip",      # ignore les lignes mal formées (ex : ta ligne 23)
    )
    return df


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Renommer les colonnes en snake_case propre."""
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def normalize_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoyer les valeurs textuelles vides / pseudo-vides."""
    df = df.copy()
    df = df.replace({"": None, "None": None, "NaN": None, "nan": None})
    return df


def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """Conversion des types : entiers, dates, montants, booléens."""
    df = df.copy()

    # id_client -> entier nullable
    if "id_client" in df.columns:
        df["id_client"] = pd.to_numeric(df["id_client"], errors="coerce").astype("Int64")

    # age -> entier nullable
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce").astype("Int64")

    # dates
    if "date_inscription" in df.columns:
        df["date_inscription"] = pd.to_datetime(
            df["date_inscription"],
            errors="coerce",
            dayfirst=True,  # format FR
        )

    if "derniere_connexion" in df.columns:
        df["derniere_connexion"] = pd.to_datetime(
            df["derniere_connexion"],
            errors="coerce",
            dayfirst=True,
        )

    # montant_total_eur -> float
    if "montant_total_eur" in df.columns:
        montant = df["montant_total_eur"].str.replace(" ", "", regex=False)
        montant = montant.str.replace(",", ".", regex=False)
        df["montant_total_eur"] = pd.to_numeric(montant, errors="coerce")

    # actif -> bool (oui/non, 1/0, true/false)
    if "actif" in df.columns:
        mapping_actif = {
            "oui": True,
            "non": False,
            "true": True,
            "false": False,
            "1": True,
            "0": False,
        }
        df["actif"] = (
            df["actif"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map(mapping_actif)
            .astype("boolean")
        )

    # newsletter_ok -> bool
    if "newsletter_ok" in df.columns:
        df["newsletter_ok"] = (
            df["newsletter_ok"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({"oui": True, "non": False, "true": True, "false": False})
            .astype("boolean")
        )

    return df


def drop_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Supprimer les lignes complètement vides."""
    return df.dropna(how="all")


def main() -> None:
    if not DATA_PATH.exists():
        raise SystemExit(f"Fichier introuvable : {DATA_PATH}")

    # 1) lecture
    df = load_raw_csv(DATA_PATH)

    # 2) nettoyage / typage
    df = clean_columns(df)
    df = normalize_strings(df)
    df = convert_types(df)
    df = drop_empty_rows(df)

    # 3) sauvegarde
    OUTPUT_DIR.mkdir(exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, sep=";")

    print(f"OK, fichier nettoyé sauvegardé dans : {OUTPUT_FILE}")
    print("Shape :", df.shape)
    print(df.head())


if __name__ == "__main__":
    main()
