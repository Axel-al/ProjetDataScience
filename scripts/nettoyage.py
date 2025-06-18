import os
import pandas as pd

# Colonnes d'intérêt
COLONNES_UTILES = ["AAAAMMJJHH", "T", "U", "FF", "RR1", "N", "LAT", "LON", "NUM_POSTE", "NOM_USUEL"]

# Fonction de nettoyage
def nettoyer_csv(path):
    df = pd.read_csv(path, sep=';', usecols=lambda c: c in COLONNES_UTILES, low_memory=False)

    # Conversion date
    cols = ["datetime"] + COLONNES_UTILES[1:]
    df["datetime"] = pd.to_datetime(df["AAAAMMJJHH"], format="%Y%m%d%H", errors="coerce")
    df = df[cols]

    
    # Suppression lignes vides sur les données
    df = df.dropna(how="all", subset=cols[:-4])

    return df

# Traitement automatique de tous les fichiers
def traiter_tous_les_csv(departements=["05", "21", "29"]):
    for dept in departements:
        input_dir = f".\\data\\{dept}"
        output_dir = f".\\clean_data\\{dept}"
        os.makedirs(output_dir, exist_ok=True)

        for fichier in os.listdir(input_dir):
            if fichier.endswith(".csv") or fichier.endswith(".csv.gz"):
                chemin_entree = os.path.join(input_dir, fichier)
                print(f"Traitement : {chemin_entree}")
                df_clean = nettoyer_csv(chemin_entree)

                # Nom du fichier nettoyé
                nom_sortie = fichier.replace(".csv", "_clean.csv").replace(".gz", "")
                chemin_sortie = os.path.join(output_dir, nom_sortie)
                df_clean.to_csv(chemin_sortie, index=False)

if __name__ == "__main__":
    traiter_tous_les_csv()