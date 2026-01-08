import pandas as pd

# 1) Lecture du CSV en tolérant les lignes cassées
df = pd.read_csv(
    "data.csv",
    sep=";",                  # séparateur
    dtype=str,                # tout en texte
    encoding="utf-8",         # encodage
    keep_default_na=False,    # ne pas convertir en NaN automatiquement
    on_bad_lines="skip"       # <<< IGNORER les lignes qui ont un souci
)

# 2) Nettoyage basique
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
df = df.replace({"": None})
df = df.dropna(how="all")

# 3) Sauvegarde
df.to_csv("clean_data.csv", index=False)

print("OK, clean_data.csv créé.")
print("Shape :", df.shape)
print(df.head())

