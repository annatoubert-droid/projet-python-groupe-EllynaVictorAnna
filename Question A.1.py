"""
Partie A.1 — Écrire vos premières fonctions
Lecture du CSV des taux, calcul de la moyenne (fonction maison) et du min/max.
"""

import csv


def lire_taux(chemin_csv):
    """
    Lit un fichier CSV de taux de change et renvoie une liste de couples (date, taux).

    Paramètre :
        chemin_csv (str) : chemin vers le fichier CSV à lire.

    Retour :
        list[tuple[str, float]] : liste de couples (date, taux), dans l'ordre du fichier.
    """
    couples = []
    with open(chemin_csv, newline="", encoding="utf-8") as f:
        lecteur = csv.reader(f)
        entete = next(lecteur)          # on saute la ligne d'en-tête
        colonne_taux = len(entete) - 1  # le taux est la dernière colonne du fichier

        for ligne in lecteur:
            if not ligne:                # ignore les lignes vides éventuelles
                continue
            date = ligne[0]
            taux = float(ligne[colonne_taux])
            couples.append((date, taux))

    return couples


def moyenne_taux(couples):
    """
    Calcule la moyenne arithmétique des taux contenus dans une liste de couples (date, taux),
    "à la main" (sans bibliothèque).

    Paramètre :
        couples (list[tuple[str, float]]) : liste de couples (date, taux).

    Retour :
        float : la moyenne des taux. Renvoie None si la liste est vide.
    """
    if not couples:
        return None

    somme = 0.0
    for _date, taux in couples:
        somme += taux
    return somme / len(couples)


def min_max_taux(couples):
    """
    Renvoie le couple (date, taux) du minimum et celui du maximum, parmi une liste
    de couples (date, taux).

    Paramètre :
        couples (list[tuple[str, float]]) : liste de couples (date, taux).

    Retour :
        tuple : (couple_min, couple_max), chacun de la forme (date, taux).
        Renvoie (None, None) si la liste est vide.
    """
    if not couples:
        return None, None

    couple_min = couples[0]
    couple_max = couples[0]

    for couple in couples[1:]:
        _date, taux = couple
        if taux < couple_min[1]:
            couple_min = couple
        if taux > couple_max[1]:
            couple_max = couple

    return couple_min, couple_max


if __name__ == "__main__":
    donnees = lire_taux("taux_EUR_USD.csv")

    print(f"Nombre de lignes lues : {len(donnees)}")
    print(f"Premières valeurs : {donnees[:3]}")
    print(f"Dernières valeurs : {donnees[-3:]}")

    moy = moyenne_taux(donnees)
    print(f"\nMoyenne (fonction maison) : {moy:.4f}")

    mini, maxi = min_max_taux(donnees)
    print(f"Taux minimum : {mini[1]} (le {mini[0]})")
    print(f"Taux maximum : {maxi[1]} (le {maxi[0]})")
