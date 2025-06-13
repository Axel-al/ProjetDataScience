import pandas as pd
import os

# Colonnes utiles (à adapter si besoin)
colonnes_utiles = [
    'NUM_POSTE', 'datetime', 'T', 'QT', 'TX', 'QTX', 'TN', 'QTN',
    'U', 'QU', 'FF', 'QFF', 'N', 'QN', 'RR1', 'QRR1', 'PMER', 'QPMER'
]

# Dossiers
input_root = './datas'
output_root = './clean_data'

# Fonction de traitement d’un fichier
def nettoyer_et_sauvegarder(fichier_entree, fichier_sortie, departement):
    print(f"Traitement de {fichier_entree}...")
    df = pd.read_csv(fichier_entree, sep=';', low_memory=False)

    # Conversion datetime
    df['datetime'] = pd.to_datetime(df['AAAAMMJJHH'], format='%Y%m%d%H', errors='coerce')
    df.drop(columns=['AAAAMMJJHH'], inplace=True)

    # Ajout du département
    df['Département'] = departement

    # On garde uniquement les colonnes utiles si elles existent
    colonnes_presentes = [col for col in colonnes_utiles if col in df.columns]
    colonnes_finales = ['Département'] + colonnes_presentes
    df = df[colonnes_finales]

    # Drop des lignes avec NaN dans les colonnes essentielles
    colonnes_critiques = ['datetime', 'T', 'U', 'FF', 'N', 'PMER']
    colonnes_critiques = [col for col in colonnes_critiques if col in df.columns]
    df.dropna(subset=colonnes_critiques, inplace=True)

    # Sauvegarde compressée
    df.to_csv(fichier_sortie, sep=';', index=False, compression='gzip')
    print(f" → Sauvé dans {fichier_sortie}")

# Traitement de tous les fichiers
for dir in os.listdir(input_root):
    input_path = os.path.join(input_root, dir)
    if not os.path.isdir(input_path):
        continue

    output_path = os.path.join(output_root, dir)
    os.makedirs(output_path, exist_ok=True)

    for file in os.listdir(input_path):
        if not file.endswith('.csv.gz'):
            continue

        fichier_entree = os.path.join(input_path, file)
        fichier_sortie = os.path.join(output_path, file)

        nettoyer_et_sauvegarder(fichier_entree, fichier_sortie, dir)
