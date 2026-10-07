"""
TD : pandas -> numpy -> polars
================================

D.1 - Du DataFrame au tableau numpy
D.2 - Comprendre numpy (dtype, broadcasting)
D.3 - Apercu de polars (comparaison avec pandas)
"""

import time

import numpy as np
import pandas as pd
import polars as pl

# ---------------------------------------------------------------------------
# Donnees d'exemple : un taux de change sur 10 jours
# ---------------------------------------------------------------------------

dates = pd.date_range("2024-01-01", periods=10, freq="D")
taux_valeurs = [1.10, 1.12, 1.11, 1.09, 1.13, 1.15, 1.14, 1.16, 1.12, 1.10]

df = pd.DataFrame({
    "date": dates,
    "taux": taux_valeurs,
})


# ---------------------------------------------------------------------------
# D.1 - Du DataFrame au tableau numpy
# ---------------------------------------------------------------------------

def d1_dataframe_vers_numpy(df: pd.DataFrame) -> None:
    print("=" * 70)
    print("D.1 - Du DataFrame au tableau numpy")
    print("=" * 70)

    # Conversion de la colonne en tableau numpy
    taux = df["taux"].to_numpy()
    print("Tableau numpy :", taux)
    print("Type :", type(taux))

    # Calculs vectorises, sans boucle for
    moyenne = taux.mean()
    ecart_type = taux.std()

    # Variations jour a jour : taux[i] - taux[i-1] pour chaque i
    variations = np.diff(taux)

    # Variations en pourcentage
    variations_pct = np.diff(taux) / taux[:-1] * 100

    print("Moyenne :", moyenne)
    print("Ecart-type :", ecart_type)
    print("Variations jour a jour :", variations)
    print("Variations jour a jour (%) :", variations_pct)
    print()

    return taux, moyenne


# ---------------------------------------------------------------------------
# D.2 - Comprendre numpy : dtype et broadcasting
# ---------------------------------------------------------------------------

def d2_dtype_et_broadcasting(taux: np.ndarray, moyenne: float) -> None:
    print("=" * 70)
    print("D.2 - Comprendre numpy : dtype et broadcasting")
    print("=" * 70)

    # dtype : le type des elements du tableau
    print("dtype de taux :", taux.dtype)  # float64

    entiers = np.array([1, 2, 3])
    print("dtype de entiers :", entiers.dtype)  # int64

    # Broadcasting : operation entre un tableau et un seul nombre
    taux_pourcent = taux * 100
    print("taux * 100 :", taux_pourcent)

    # Autre exemple : centrer les donnees (soustraire la moyenne)
    taux_centre = taux - moyenne
    print("taux - moyenne :", taux_centre)
    print()


# ---------------------------------------------------------------------------
# D.3 - Apercu de polars
# ---------------------------------------------------------------------------

def d3_apercu_polars(dates: pd.DatetimeIndex, taux_valeurs: list) -> None:
    print("=" * 70)
    print("D.3 - Apercu de polars")
    print("=" * 70)

    df_pl = pl.DataFrame({
        "date": dates,
        "taux": taux_valeurs,
    })

    # Moyenne et ecart-type
    moyenne_pl = df_pl["taux"].mean()
    ecart_type_pl = df_pl["taux"].std()

    # Variation jour a jour
    df_pl = df_pl.with_columns(
        (pl.col("taux") - pl.col("taux").shift(1)).alias("variation")
    )

    print(df_pl)
    print("Moyenne (polars) :", moyenne_pl)
    print("Ecart-type (polars) :", ecart_type_pl)

    # Regroupement : moyenne du taux par mois
    df_pl_group = (
        df_pl
        .with_columns(pl.col("date").dt.month().alias("mois"))
        .group_by("mois")
        .agg(pl.col("taux").mean().alias("taux_moyen"))
    )
    print(df_pl_group)
    print()


# ---------------------------------------------------------------------------
# Comparaison des temps d'execution pandas vs polars
# ---------------------------------------------------------------------------

def comparaison_temps_execution(n: int = 1_000_000) -> None:
    print("=" * 70)
    print(f"Comparaison des temps d'execution (n = {n:,} lignes)")
    print("=" * 70)

    gros_df_pd = pd.DataFrame({"taux": np.random.uniform(0.9, 1.3, n)})
    gros_df_pl = pl.DataFrame({"taux": gros_df_pd["taux"].to_numpy()})

    t0 = time.time()
    gros_df_pd["taux"].mean()
    print("pandas :", time.time() - t0, "secondes")

    t0 = time.time()
    gros_df_pl["taux"].mean()
    print("polars :", time.time() - t0, "secondes")
    print()


# ---------------------------------------------------------------------------
# Point d'entree
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    taux_np, moyenne_np = d1_dataframe_vers_numpy(df)
    d2_dtype_et_broadcasting(taux_np, moyenne_np)
    d3_apercu_polars(dates, taux_valeurs)
    comparaison_temps_execution()
