import pandas as pd

def statistiques_base(serie):
    """
    Calcule les statistiques descriptives de base pour une série numérique.

    Paramètres
    ----------
    serie : pandas.Series
        La série de données numériques pour laquelle calculer les statistiques.

    Retours
    -------
    dict
        Un dictionnaire contenant les statistiques suivantes :
        - 'min' : valeur minimale
        - 'Q1' : premier quartile (25%)
        - 'médiane' : médiane (50%)
        - 'Q3' : troisième quartile (75%)
        - 'max' : valeur maximale
        - 'moyenne' : moyenne arithmétique
        - 'écart-type' : écart-type
        - 'écart-type relatif' : écart-type relatif en pourcentage (None si la moyenne est nulle)
    """
    return {
        "min": serie.min(),
        "Q1": serie.quantile(0.25),
        "médiane": serie.median(),
        "Q3": serie.quantile(0.75),
        "max": serie.max(),
        "moyenne": serie.mean(),
        "écart-type": serie.std(),
        "écart-type relatif": (serie.std() / serie.mean() * 100) if serie.mean() != 0 else None
    }

def resample_mensuel(df, variable):
    """Retourne la moyenne mensuelle d'une variable."""
    return df.set_index("datetime")[variable].resample("ME").mean()

def extraire_points(df, variables):
    """
    Extrait une liste de points à afficher sur la carte, à partir d’un DataFrame contenant les colonnes :
    'LAT', 'LON', 'NUM_POSTE' ou 'NOM_USUEL', ainsi que les variables météo à moyenner.

    Chaque point est un dictionnaire contenant :
    - 'lat' : latitude
    - 'lon' : longitude
    - 'nom' : nom de la station
    - une ou plusieurs variables moyennées, si disponibles
    """

    points = []
    nom_col = "NUM_POSTE" if "NUM_POSTE" in df.columns else "NOM_USUEL"
    for nom_station in df[nom_col].unique():
        df_station = df[df[nom_col] == nom_station]
        point = {
            "lat": df_station["LAT"].iloc[0],
            "lon": df_station["LON"].iloc[0],
            "nom": nom_station
        }
        for col in variables:
            valeur = df_station[col].mean()
            if not pd.isna(valeur):
                point[col] = round(valeur, 2)
        points.append(point)
    return points