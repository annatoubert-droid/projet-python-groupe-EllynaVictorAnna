"""
Partie B.1 - try/except
"""

import json
import os
import urllib.error
import urllib.request


BASE = "EUR"
DEVISE = "THB"
DEBUT = "2026-01-01"
FIN = "2026-09-01"

API = "https://api.frankfurter.app"

DOSSIER = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(DOSSIER, "cache")
DONNEES = os.path.join(DOSSIER, "donnees")


def telecharger(url):
    """
    Appelle l'URL et renvoie (texte_brut, dictionnaire Python).

    Trois familles d'erreurs sont gerees separement :
        - HTTPError : le serveur a repondu, mais avec un code d'erreur
          (403, 404, 500...). A tester AVANT URLError, car HTTPError en
          est une sous-classe.
        - URLError : pas de reponse du tout (pas de connexion, serveur
          injoignable, nom de domaine introuvable...).
        - JSONDecodeError : une reponse a bien ete recue, mais ce n'est
          pas du JSON valide (page d'erreur HTML, reponse tronquee...).

    Retour :
        (brut, donnees) si tout s'est bien passe ;
        (None, None) en cas d'erreur, avec un message clair affiche,
        sans jamais arreter brutalement le programme.
    """
    print("Appel :", url)

    try:
        with urllib.request.urlopen(url, timeout=10) as reponse:
            brut = reponse.read().decode("utf-8")

    except urllib.error.HTTPError as erreur:
        print(f"Erreur : le serveur a repondu avec le code {erreur.code}.")
        return None, None

    except urllib.error.URLError as erreur:
        print("Erreur : impossible de joindre le serveur (verifiez la connexion).")
        print("         detail :", erreur.reason)
        return None, None

    try:
        donnees = json.loads(brut)
    except json.JSONDecodeError:
        print("Erreur : la reponse du serveur est illisible.")
        return None, None

    return brut, donnees


# --- 1) Taux du jour ----------------------------------------------------------

def taux_du_jour():
    """Recupere le taux du jour EUR -> DEVISE. Renvoie (None, None) si echec."""
    url = API + "/latest?from=" + BASE + "&to=" + DEVISE
    brut, donnees = telecharger(url)

    if donnees is None:
        print("=> Taux du jour indisponible, on abandonne cette etape.")
        return None, None

    date = donnees["date"]
    taux = donnees["rates"][DEVISE]

    print("Date  :", date)
    print("Taux  : 1 " + BASE + " = " + str(taux) + " " + DEVISE)

    chemin = os.path.join(CACHE, "latest_" + BASE + "_" + DEVISE + ".json")
    with open(chemin, "w", encoding="utf-8") as fichier:
        fichier.write(brut)

    return date, taux


# --- 2) Serie sur une periode --------------------------------------------------

def serie():
    """Recupere la serie EUR -> DEVISE entre DEBUT et FIN. Renvoie ([], {}) si echec."""
    url = API + "/" + DEBUT + ".." + FIN + "?from=" + BASE + "&to=" + DEVISE
    brut, donnees = telecharger(url)

    if donnees is None:
        print("=> Serie indisponible, on abandonne cette etape.")
        return [], {}

    nom_cache = "serie_" + BASE + "_" + DEVISE + "_" + DEBUT + "_" + FIN + ".json"
    chemin_cache = os.path.join(CACHE, nom_cache)
    with open(chemin_cache, "w", encoding="utf-8") as fichier:
        fichier.write(brut)

    rates = donnees.get("rates", {})
    dates = sorted(rates.keys())

    nom_csv = "taux_" + BASE + "_" + DEVISE + ".csv"
    chemin_csv = os.path.join(DONNEES, nom_csv)
    with open(chemin_csv, "w", encoding="utf-8") as fichier:
        fichier.write("date," + DEVISE + "\n")
        for d in dates:
            fichier.write(d + "," + str(rates[d][DEVISE]) + "\n")

    print("CSV ecrit dans :", chemin_csv)
    print("Nombre de jours ouvres :", len(dates))
    if dates:
        print("Premier jour :", dates[0], "->", rates[dates[0]][DEVISE])
        print("Dernier jour :", dates[-1], "->", rates[dates[-1]][DEVISE])

    return dates, rates


# --- Programme principal -------------------------------------------------------

def main():
    for dossier in (CACHE, DONNEES):
        if not os.path.isdir(dossier):
            os.makedirs(dossier)

    print("=== 1) Taux du jour ===")
    taux_du_jour()

    print()
    print("=== 2) Serie du " + DEBUT + " au " + FIN + " ===")
    serie()


if __name__ == "__main__":
    main()
