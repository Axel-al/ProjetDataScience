def statistiques_base(serie):
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
    return df.set_index("datetime")[variable].resample("M").mean()