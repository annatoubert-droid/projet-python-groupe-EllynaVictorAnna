"""Séance 3 — Partie B : nettoyer, consolider et analyser les taux avec pandas.

À adapter : FICHIER_CSV, COL_DATE et COL_TAUX doivent correspondre au CSV
produit à la séance 1 (nom du fichier et noms des colonnes).
Ce code est à intégrer dans analyse.py (livrable de la séance).
"""

import pandas as pd

# ---------------------------------------------------------------------------
# Paramètres à adapter à votre CSV
# ---------------------------------------------------------------------------
FICHIER_CSV = "taux.csv"   # chemin du CSV de la séance 1
COL_DATE = "date"          # nom de la colonne des dates
COL_TAUX = "taux"          # nom de la colonne des taux

# Fréquence « fin de mois » : "ME" depuis pandas 2.2, "M" avant.
_version = tuple(int(x) for x in pd.__version__.split(".")[:2])
FREQ_MOIS = "ME" if _version >= (2, 2) else "M"


# ---------------------------------------------------------------------------
# Chargement (rappel de la partie A)
# ---------------------------------------------------------------------------
def charger_taux(chemin: str) -> pd.Series:
    """Charge le CSV et renvoie une Series de taux indexée par la date."""
    # parse_dates : convertit la colonne texte en vraies dates (datetime64).
    # Sans cela, l'index serait du texte et reindex / resample ne marcheraient pas.
    df = pd.read_csv(chemin, parse_dates=[COL_DATE])

    # La date devient l'index, et on trie chronologiquement
    # (forward-fill, rolling et resample supposent un ordre croissant).
    df = df.set_index(COL_DATE).sort_index()

    # reindex plante si une date apparaît deux fois : on vérifie avant.
    if not df.index.is_unique:
        raise ValueError("L'index contient des dates en double : nettoyer d'abord.")

    return df[COL_TAUX]  # une Series (une seule colonne)


# ---------------------------------------------------------------------------
# B.1 — Combler les trous (jours ouvrés + forward-fill)
# ---------------------------------------------------------------------------
def combler_trous(taux: pd.Series) -> pd.Series:
    """Réindexe sur un calendrier continu de jours ouvrés et propage la dernière valeur connue."""
    # 1) Calendrier continu de jours ouvrés (lundi -> vendredi) entre la première
    #    et la dernière date du fichier.
    calendrier = pd.bdate_range(start=taux.index.min(), end=taux.index.max(), name=COL_DATE)

    # 2) reindex : la Series prend exactement les dates du calendrier.
    #    - date déjà présente  -> on garde sa valeur ;
    #    - date absente (ex. jour férié) -> NaN.
    #    Attention : une éventuelle date de week-end du fichier serait supprimée.
    taux_reindexe = taux.reindex(calendrier)

    nb_trous = int(taux_reindexe.isna().sum())
    nb_ecartes = len(taux) - int(taux_reindexe.notna().sum())
    print(f"Jours ouvrés du calendrier : {len(calendrier)}")
    print(f"Trous créés par le reindex (NaN) : {nb_trous}")
    print(f"Dates du fichier hors calendrier (week-ends) : {nb_ecartes}")

    # 3) Forward-fill : chaque NaN reçoit la dernière valeur connue avant lui.
    #    Pas de NaN en tête de série : le calendrier commence à la 1re date du fichier.
    taux_complet = taux_reindexe.ffill()

    print(f"NaN restants après ffill : {int(taux_complet.isna().sum())}")
    return taux_complet


# ---------------------------------------------------------------------------
# B.2 — Analyser
# ---------------------------------------------------------------------------
def variation_periode(taux: pd.Series) -> float:
    """Variation en % entre le premier et le dernier taux de la période."""
    premier = taux.iloc[0]    # iloc : accès par position (0 = première ligne)
    dernier = taux.iloc[-1]   # -1 = dernière ligne
    return (dernier - premier) / premier * 100


def variations_journalieres(taux: pd.Series) -> pd.Series:
    """Variation en % d'un jour ouvré au suivant (la 1re valeur est NaN)."""
    # pct_change() calcule (x_t - x_{t-1}) / x_{t-1}
    return taux.pct_change() * 100


def moyenne_mobile(taux: pd.Series, fenetre: int) -> pd.Series:
    """Moyenne mobile simple sur `fenetre` jours ouvrés."""
    # rolling(window=n) : fenêtre glissante des n dernières valeurs ;
    # .mean() : moyenne de chaque fenêtre. Les n-1 premières valeurs sont NaN
    # car la fenêtre n'est pas encore pleine.
    return taux.rolling(window=fenetre).mean()


def resample_mensuel(taux: pd.Series) -> pd.DataFrame:
    """Rééchantillonne en données mensuelles (moyenne, dernier jour, variation)."""
    # resample : regroupe les lignes par mois (l'index doit être une date), puis
    # on choisit comment résumer chaque mois.
    rs = taux.resample(FREQ_MOIS)

    mensuel = pd.DataFrame({
        "moyenne": rs.mean(),                      # taux moyen du mois
        "fin_de_mois": rs.last(),                  # dernier taux du mois
        "min": rs.min(),
        "max": rs.max(),
    })
    # Variation en % d'un mois à l'autre (sur le taux de fin de mois)
    mensuel["variation_mensuelle_%"] = mensuel["fin_de_mois"].pct_change() * 100
    return mensuel


# ---------------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------------
def main() -> None:
    taux = charger_taux(FICHIER_CSV)

    # --- B.1 ---
    taux_complet = combler_trous(taux)

    # --- B.2 ---
    var = variation_periode(taux_complet)
    print(f"\nVariation sur la période : {var:.2f} %")

    var_jour = variations_journalieres(taux_complet)
    print("\nVariations journalières (%) — résumé :")
    print(var_jour.describe())

    mm5 = moyenne_mobile(taux_complet, 5)     # ~ 1 semaine de jours ouvrés
    mm20 = moyenne_mobile(taux_complet, 20)   # ~ 1 mois de jours ouvrés
    print("\nTaux et moyennes mobiles (5 et 20 jours) — dernières lignes :")
    print(pd.DataFrame({"taux": taux_complet, "mm5": mm5, "mm20": mm20}).tail())

    mensuel = resample_mensuel(taux_complet)
    print("\nDonnées mensuelles :")
    print(mensuel)


if __name__ == "__main__":
    main()
