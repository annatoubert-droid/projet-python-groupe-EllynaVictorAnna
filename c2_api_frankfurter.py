# -*- coding: utf-8 -*-
"""
C.2 - Appeler l'API pour de vrai
API Frankfurter (taux de change de reference de la BCE, base euro, sans cle).
    https://api.frankfurter.app  -  doc : https://frankfurter.dev
Devise du groupe : THB (baht thailandais)

1. Taux du jour   : /latest?from=EUR&to=THB
2. Serie 01/01/2026 -> 01/09/2026 : /2026-01-01..2026-09-01?from=EUR&to=THB
   -> reponse brute enregistree dans cache/
   -> version simple en CSV (une ligne par date) dans donnees/
Python de base uniquement : urllib.request, json, os.
"""

import json
import os
import urllib.request

# --- Parametres -------------------------------------------------------------

BASE = "EUR"          # devise de base (parametre from)
DEVISE = "THB"        # devise du groupe (parametre to)
DEBUT = "2026-01-01"
FIN = "2026-09-01"

API = "https://api.frankfurter.app"

# Les dossiers cache/ et donnees/ sont a cote du script, quel que soit
# le repertoire depuis lequel on lance le programme.
DOSSIER = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(DOSSIER, "cache")
DONNEES = os.path.join(DOSSIER, "donnees")


def telecharger(url):
    """Appelle l'URL et renvoie (texte_brut, dictionnaire Python)."""
    with urllib.request.urlopen(url) as reponse:
        brut = reponse.read().decode("utf-8")
    return brut, json.loads(brut)


# --- 1) Taux du jour --------------------------------------------------------

def taux_du_jour():
    url = API + "/latest?from=" + BASE + "&to=" + DEVISE
    print("Appel :", url)

    brut, donnees = telecharger(url)

    # Meme forme que le dictionnaire de la partie C.1 :
    # {"amount": 1.0, "base": "EUR", "date": "...", "rates": {"THB": ...}}
    date = donnees["date"]
    taux = donnees["rates"][DEVISE]

    print("Date  :", date)
    print("Taux  : 1 " + BASE + " = " + str(taux) + " " + DEVISE)

    # On garde aussi la reponse brute dans cache/
    chemin = os.path.join(CACHE, "latest_" + BASE + "_" + DEVISE + ".json")
    fichier = open(chemin, "w", encoding="utf-8")
    fichier.write(brut)
    fichier.close()

    return date, taux


# --- 2) Serie sur une periode ----------------------------------------------

def serie():
    url = (API + "/" + DEBUT + ".." + FIN
           + "?from=" + BASE + "&to=" + DEVISE)
    print()
    print("Appel :", url)

    brut, donnees = telecharger(url)

    # a) reponse brute dans cache/
    nom_cache = ("serie_" + BASE + "_" + DEVISE + "_"
                 + DEBUT + "_" + FIN + ".json")
    chemin_cache = os.path.join(CACHE, nom_cache)
    fichier = open(chemin_cache, "w", encoding="utf-8")
    fichier.write(brut)
    fichier.close()
    print("Reponse brute enregistree dans :", chemin_cache)

    # b) version simple en CSV dans donnees/ (une ligne par date)
    # Ici "rates" est indexe par date : {"2026-01-02": {"THB": ...}, ...}
    rates = donnees["rates"]
    dates = sorted(rates.keys())   # tri chronologique (format AAAA-MM-JJ)

    nom_csv = "taux_" + BASE + "_" + DEVISE + ".csv"
    chemin_csv = os.path.join(DONNEES, nom_csv)
    fichier = open(chemin_csv, "w", encoding="utf-8")
    fichier.write("date," + DEVISE + "\n")
    for d in dates:
        fichier.write(d + "," + str(rates[d][DEVISE]) + "\n")
    fichier.close()

    print("CSV ecrit dans :", chemin_csv)
    print("Nombre de jours ouvres :", len(dates))
    if dates:
        print("Premier jour :", dates[0], "->", rates[dates[0]][DEVISE])
        print("Dernier jour :", dates[-1], "->", rates[dates[-1]][DEVISE])

    return dates, rates


# --- Programme principal ----------------------------------------------------

def main():
    # On s'assure que les dossiers existent
    if not os.path.isdir(CACHE):
        os.makedirs(CACHE)
    if not os.path.isdir(DONNEES):
        os.makedirs(DONNEES)

    print("=== 1) Taux du jour ===")
    taux_du_jour()

    print()
    print("=== 2) Serie du " + DEBUT + " au " + FIN + " ===")
    serie()


if __name__ == "__main__":
    main()
