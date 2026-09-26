"""Séance 3 — Partie C : les jointures avec pandas.

À adapter : les chemins des deux CSV, les noms de devises et les noms de colonnes
doivent correspondre à vos fichiers de la séance 1.
Ce code est à intégrer dans analyse.py (livrable de la séance).
"""

import pandas as pd

# ---------------------------------------------------------------------------
# Paramètres à adapter
# ---------------------------------------------------------------------------
FICHIER_DEVISE_1 = "taux_usd.csv"   # CSV de la 1re devise de votre groupe
FICHIER_DEVISE_2 = "taux_gbp.csv"   # CSV de la 2e devise de votre groupe
DEVISE_1 = "USD"
DEVISE_2 = "GBP"
COL_DATE = "date"                   # nom de la colonne des dates
COL_TAUX = "taux"                   # nom de la colonne des taux


def charger_devise(chemin: str, nom_devise: str) -> pd.DataFrame:
    """Charge le CSV d'une devise : un DataFrame avec les colonnes date et taux_<devise>."""
    df = pd.read_csv(chemin, parse_dates=[COL_DATE])

    # On garde uniquement la date et le taux, et on renomme la colonne du taux.
    # Pourquoi renommer ? Si les deux DataFrames ont une colonne "taux", la jointure
    # ne saurait pas les distinguer et ajouterait des suffixes _x / _y illisibles.
    df = df[[COL_DATE, COL_TAUX]].rename(columns={COL_TAUX: f"taux_{nom_devise}"})

    # Ici la date reste une COLONNE (pas l'index) : merge joint sur une colonne clé.
    return df


# ---------------------------------------------------------------------------
# C.1 — Réunir deux séries de taux
# ---------------------------------------------------------------------------
def reunir_deux_devises(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """Réunit les deux devises en un seul DataFrame indexé par date."""
    print(f"Lignes devise 1 : {len(df1)} | lignes devise 2 : {len(df2)}")

    # merge : associe les lignes qui ont la même valeur dans la colonne clé `on`.
    #  - on=COL_DATE  : la clé de jointure est la date ;
    #  - how="inner"  : on ne garde que les dates présentes dans les deux tables.
    #    Sur la même période les dates coïncident, donc aucune ligne n'est perdue ;
    #  - validate="one_to_one" : pandas plante si une date apparaît deux fois dans
    #    l'une des tables. C'est un garde-fou contre la duplication de lignes.
    fusion = pd.merge(df1, df2, on=COL_DATE, how="inner", validate="one_to_one")

    # Vérification demandée par l'énoncé : le nombre de lignes après le merge.
    print(f"Lignes après le merge : {len(fusion)}")
    if not (len(fusion) == len(df1) == len(df2)):
        print("Attention : les dates ne coïncident pas parfaitement, des lignes ont été perdues.")

    # On met la date en index et on trie : on obtient un DataFrame indexé par date.
    fusion = fusion.set_index(COL_DATE).sort_index()
    print(fusion.head())
    return fusion


# ---------------------------------------------------------------------------
# C.2 — Les types de jointure (exemple de l'énoncé)
# ---------------------------------------------------------------------------
def types_de_jointure() -> None:
    """Compare inner, left, right et outer sur deux petites tables aux clés partiellement communes."""
    # Table de gauche : clés {1, 2} ; table de droite : clés {2, 3}.
    # Seule la clé 2 est commune aux deux tables.
    gauche = pd.DataFrame({"cle": [1, 2], "valeur_gauche": ["a", "b"]})
    droite = pd.DataFrame({"cle": [2, 3], "valeur_droite": ["x", "y"]})
    print("Table de gauche :")
    print(gauche)
    print("\nTable de droite :")
    print(droite)

    for how in ["inner", "left", "right", "outer"]:
        # indicator=True ajoute une colonne _merge qui indique l'origine de chaque
        # ligne : both / left_only / right_only. Pratique pour voir où sont les NaN.
        resultat = pd.merge(gauche, droite, on="cle", how=how, indicator=True)
        print(f"\n--- how='{how}' ---")
        print(resultat)
    # Attendu :
    #   inner -> clés {2}
    #   left  -> clés {1, 2}    (NaN à droite pour la clé 1)
    #   right -> clés {2, 3}    (NaN à gauche pour la clé 3)
    #   outer -> clés {1, 2, 3} (NaN de chaque côté là où il manque une correspondance)


def duplication_de_cles() -> None:
    """Montre le piège de la duplication : 2 lignes à gauche x 3 à droite = 6 lignes."""
    gauche = pd.DataFrame({"cle": [1, 1], "valeur_gauche": ["a", "b"]})           # clé 1 deux fois
    droite = pd.DataFrame({"cle": [1, 1, 1], "valeur_droite": ["x", "y", "z"]})   # clé 1 trois fois

    resultat = pd.merge(gauche, droite, on="cle", how="inner")
    print(f"\nDuplication : {len(gauche)} lignes à gauche, {len(droite)} à droite "
          f"-> {len(resultat)} lignes après le merge")
    print(resultat)


# ---------------------------------------------------------------------------
# C.3 — merge, join ou concat ?
# ---------------------------------------------------------------------------
def merge_join_concat(df1: pd.DataFrame, df2: pd.DataFrame) -> None:
    """Compare les trois façons d'assembler des tables (df1 et df2 ont la date en colonne)."""
    # 1) merge : joint sur une COLONNE clé (ici la date). Par défaut how="inner".
    par_merge = pd.merge(df1, df2, on=COL_DATE)
    print(f"merge  : {par_merge.shape[0]} lignes, {par_merge.shape[1]} colonnes")

    # 2) join : joint sur l'INDEX. On met donc d'abord la date en index.
    #    Attention : par défaut how="left" (et non "inner" comme merge).
    par_join = df1.set_index(COL_DATE).join(df2.set_index(COL_DATE), how="inner")
    print(f"join   : {par_join.shape[0]} lignes, {par_join.shape[1]} colonnes")

    # 3) concat : assemble sans apparier de clé par colonne.
    #    a) axis=1 : côte à côte, les lignes sont alignées sur l'index (la date ici).
    cote_a_cote = pd.concat([df1.set_index(COL_DATE), df2.set_index(COL_DATE)], axis=1)
    print(f"concat (axis=1) : {cote_a_cote.shape[0]} lignes, {cote_a_cote.shape[1]} colonnes")

    #    b) axis=0 (par défaut) : les unes sous les autres. On coupe df1 en deux
    #       moitiés (début et fin de période) puis on les rempile.
    milieu = len(df1) // 2
    debut, fin = df1.iloc[:milieu], df1.iloc[milieu:]
    empile = pd.concat([debut, fin], ignore_index=True)   # ignore_index : renumérote 0..n-1
    print(f"concat (axis=0) : {empile.shape[0]} lignes, {empile.shape[1]} colonnes "
          f"(identique à df1 : {empile.equals(df1.reset_index(drop=True))})")

    # Résumé : merge/join APPARIENT des lignes selon une clé (colonne ou index),
    # concat EMPILE des tables sans clé : sous les unes des autres, ou côte à côte
    # en alignant sur l'index.


# ---------------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------------
def main() -> None:
    df1 = charger_devise(FICHIER_DEVISE_1, DEVISE_1)
    df2 = charger_devise(FICHIER_DEVISE_2, DEVISE_2)

    print("=== C.1 — Réunir les deux devises ===")
    devises = reunir_deux_devises(df1, df2)

    print("\n=== C.2 — Types de jointure ===")
    types_de_jointure()
    duplication_de_cles()

    print("\n=== C.3 — merge, join, concat ===")
    merge_join_concat(df1, df2)


if __name__ == "__main__":
    main()
