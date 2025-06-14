import os
import pandas as pd

# Colonnes d'intérêt
COLONNES_UTILES = ["AAAAMMJJHH", "T", "U", "FF", "RR1", "N"]

# Fonction de nettoyage
def nettoyer_csv(path):
    df = pd.read_csv(path, sep=';', usecols=lambda c: c in COLONNES_UTILES, low_memory=False)

    # Conversion date
    df["AAAAMMJJHH"] = pd.to_datetime(df["AAAAMMJJHH"], format="%Y%m%d%H", errors="coerce")

    # Suppression lignes avec date invalide
    df = df.dropna(subset=["AAAAMMJJHH"])

    # Suppression lignes vides sur les données
    df = df.dropna(how="all", subset=["T", "U", "FF", "RR1", "N"])

    return df

# Traitement automatique de tous les fichiers
def traiter_tous_les_csv(departements=["05", "21", "29"]):
    for dept in departements:
        input_dir = f"./data/{dept}"
        output_dir = f"./clean_data/{dept}"
        os.makedirs(output_dir, exist_ok=True)

        for fichier in os.listdir(input_dir):
            if fichier.endswith(".csv") or fichier.endswith(".csv.gz"):
                chemin_entree = os.path.join(input_dir, fichier)
                print(f"Traitement : {chemin_entree}")
                df_clean = nettoyer_csv(chemin_entree)

                # Nom du fichier nettoyé
                nom_sortie = fichier.replace(".csv", "_clean.csv").replace(".csv.gz", "_clean.csv")
                chemin_sortie = os.path.join(output_dir, nom_sortie)
                df_clean.to_csv(chemin_sortie, index=False)