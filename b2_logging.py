# -*- coding: utf-8 -*-
"""
Partie B.2 - logging
Reprend B.1 (l'appel API protege par try/except) et remplace les print()
de suivi par du logging : fichier de log, niveaux info / warning / error.
Devise du groupe : THB (baht thailandais)
"""

import json
import logging
import os
import urllib.error
import urllib.request

# --- Parametres -------------------------------------------------------------

BASE = "EUR"
DEVISE = "THB"
DEBUT = "2026-01-01"
FIN = "2026-09-01"

API = "https://api.frankfurter.app"

DOSSIER = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(DOSSIER, "cache")
DONNEES = os.path.join(DOSSIER, "donnees")
LOGS = os.path.join(DOSSIER, "logs")


def configurer_logging():
    """
    Configure le logging pour tout le programme : ecrit dans le fichier
    logs/api_frankfurter.log, avec la date/heure, le niveau et le message.
    Niveau minimum affiche : INFO (donc INFO, WARNING et ERROR sont ecrits,
    DEBUG est ignore).
    """
    if not os.path.isdir(LOGS):
        os.makedirs(LOGS)

    chemin_log = os.path.join(LOGS, "api_frankfurter.log")

    logging.basicConfig(
        filename=chemin_log,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8",
    )


def telecharger(url):
    """
    Appelle l'URL et renvoie (texte_brut, dictionnaire Python).
    Meme gestion des erreurs qu'en B.1, mais chaque etape est desormais
    journalisee au lieu d'etre seulement affichee.
    """
    logging.info("Appel de l'API : %s", url)

    try:
        with urllib.request.urlopen(url, timeout=10) as reponse:
            brut = reponse.read().decode("utf-8")

    except urllib.error.HTTPError as erreur:
        logging.error("Erreur HTTP %s en appelant %s", erreur.code, url)
        print(f"Erreur : le serveur a repondu avec le code {erreur.code}.")
        return None, None

    except urllib.error.URLError as erreur:
        logging.error("Impossible de joindre le serveur (%s) : %s", url, erreur.reason)
        print("Erreur : impossible de joindre le serveur (verifiez la connexion).")
        return None, None

    try:
        donnees = json.loads(brut)
    except json.JSONDecodeError:
        logging.error("Reponse recue mais illisible (JSON invalide) pour %s", url)
        print("Erreur : la reponse du serveur est illisible.")
        return None, None

    logging.info("Reponse recue et decodee avec succes (%d caracteres).", len(brut))
    return brut, donnees


# --- 1) Taux du jour ----------------------------------------------------------

def taux_du_jour():
    """Recupere le taux du jour EUR -> DEVISE. Renvoie (None, None) si echec."""
    url = API + "/latest?from=" + BASE + "&to=" + DEVISE
    brut, donnees = telecharger(url)

    if donnees is None:
        logging.warning("Taux du jour indisponible : on abandonne cette etape.")
        return None, None

    date = donnees["date"]
    taux = donnees["rates"][DEVISE]

    print("Date  :", date)
    print("Taux  : 1 " + BASE + " = " + str(taux) + " " + DEVISE)
    logging.info("Taux du jour recupere : 1 %s = %s %s (%s)", BASE, taux, DEVISE, date)

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
        logging.warning("Serie indisponible : on abandonne cette etape.")
        return [], {}

    nom_cache = "serie_" + BASE + "_" + DEVISE + "_" + DEBUT + "_" + FIN + ".json"
    chemin_cache = os.path.join(CACHE, nom_cache)
    with open(chemin_cache, "w", encoding="utf-8") as fichier:
        fichier.write(brut)

    rates = donnees.get("rates", {})
    if not rates:
        # cas suspect : l'appel a reussi mais il n'y a aucune donnee dedans
        logging.warning("La reponse ne contient aucune date de taux (rates vide).")

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

    logging.info(
        "Serie enregistree : %d jours (du %s au %s).",
        len(dates),
        dates[0] if dates else "?",
        dates[-1] if dates else "?",
    )

    return dates, rates


# --- Programme principal -------------------------------------------------------

def main():
    configurer_logging()

    for dossier in (CACHE, DONNEES):
        if not os.path.isdir(dossier):
            os.makedirs(dossier)

    logging.info("=== Debut du programme ===")

    print("=== 1) Taux du jour ===")
    taux_du_jour()

    print()
    print("=== 2) Serie du " + DEBUT + " au " + FIN + " ===")
    serie()

    logging.info("=== Fin du programme ===")


if __name__ == "__main__":
    main()
