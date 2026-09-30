"""
Projet Python - Séance 4
Python idiomatique, POO, matplotlib et ligne de commande (argparse).

Ce fichier regroupe TOUS les codes de la séance (parties A à D).
Dans le dépôt final, on le découpera en modules dans src/ (voir partie D).

Utilisation (à lancer depuis la racine du dépôt) :
    python seance4.py extraire                  # télécharge THB et la 2e devise -> donnees/taux_EUR_<DEVISE>.csv
    python seance4.py analyser --devise THB     # statistiques dans le terminal
    python seance4.py graphiques                # crée les PNG dans figures/
    python seance4.py demo                      # démonstrations des parties A, B et C

Dépendance : pip install matplotlib
"""

import argparse
import csv
import json
import logging
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # pas de fenêtre : on sauvegarde directement en PNG
import matplotlib.pyplot as plt

# Paramètres repris des séances 1 et 2
BASE = "EUR"
DEVISES_GROUPE = ["THB", "USD"]  # THB = votre devise ; à vérifier / changer pour la 2e
DEBUT = "2026-01-01"
FIN = "2026-09-01"
API = "https://api.frankfurter.app"

DOSSIER_DATA = Path("donnees")
DOSSIER_LOGS = Path("logs")
DOSSIER_FIGURES = Path("figures")


# ======================================================================
# PARTIE A - Python plus idiomatique
# ======================================================================
def partie_a(dates, taux):
    print("=== PARTIE A - Python idiomatique ===")

    # ---- A.1 Compréhensions --------------------------------------
    # Version boucle classique (style séance 2)
    variations_boucle = []
    for i in range(1, len(taux)):
        variations_boucle.append((taux[i] - taux[i - 1]) / taux[i - 1] * 100)

    # Même chose en compréhension de liste
    variations = [(b - a) / a * 100 for a, b in zip(taux, taux[1:])]
    assert variations == variations_boucle

    # Compréhension de liste avec condition : seulement les hausses
    hausses = [v for v in variations if v > 0]

    # Compréhension de dictionnaire : date (texte) -> taux
    taux_par_date = {d.isoformat(): t for d, t in zip(dates, taux)}

    # Compréhension de dictionnaire avec condition : taux > moyenne
    moyenne = sum(taux) / len(taux)
    jours_au_dessus = {d: t for d, t in taux_par_date.items() if t > moyenne}

    print(f"Nombre de variations : {len(variations)}, dont {len(hausses)} hausses")
    print(f"Jours au-dessus de la moyenne : {len(jours_au_dessus)}")

    # ---- A.2 enumerate, zip, sorted ------------------------------
    # enumerate : indice + valeur
    for i, t in enumerate(taux[:3]):
        print(f"  indice {i} -> taux {t}")
    # enumerate avec départ à 1
    for rang, t in enumerate(taux[:3], start=1):
        print(f"  n°{rang} : {t}")

    # zip : associer deux listes (dates et taux)
    for d, t in list(zip(dates, taux))[:3]:
        print(f"  {d} : {t}")

    # sorted avec key : les 3 plus hauts taux, puis les dates triées par taux
    paires = list(zip(dates, taux))
    top3 = sorted(paires, key=lambda paire: paire[1], reverse=True)[:3]
    print("  Top 3 des taux :", top3)

    # sorted sur un dictionnaire : trier par valeur
    bas = sorted(taux_par_date.items(), key=lambda kv: kv[1])[:3]
    print("  3 taux les plus bas :", bas)

    # ---- A.3 f-strings, lambda, map/filter -----------------------
    d0, t0 = dates[0], taux[0]
    print(f"  Le {d0:%d/%m/%Y}, le taux valait {t0:.2f}")  # 2 décimales
    print(f"  Variation moyenne : {sum(variations) / len(variations):+.3f} %")
    print(f"  Taux avec séparateur et alignement : {t0:>10.4f}|")
    print(f"  Expression dans une f-string : {t0 * 100:.1f} centimes")

    # lambda + map : convertir les taux en pourcentage de la première valeur
    base100 = list(map(lambda x: x / taux[0] * 100, taux))
    # lambda + filter : garder les variations supérieures à 0,5 % en valeur absolue
    fortes = list(filter(lambda v: abs(v) > 0.5, variations))
    print(f"  Premier point base 100 : {base100[0]:.1f} ; fortes variations : {len(fortes)}")
    print()


# ======================================================================
# PARTIE B - Programmation orientée objet
# ======================================================================

# ---- B.1 Première classe -------------------------------------------
class SerieTaux:
    """Taux d'une devise sur une période."""

    # Attribut de CLASSE : partagé par toutes les instances
    devise_base = "EUR"

    def __init__(self, devise, dates, taux):
        # Attributs d'INSTANCE : propres à chaque objet
        self.devise = devise
        self.dates = list(dates)
        self.taux = list(taux)

    def moyenne(self):
        return sum(self.taux) / len(self.taux)

    def variations(self):
        """Variations quotidiennes en %."""
        return [(b - a) / a * 100 for a, b in zip(self.taux, self.taux[1:])]

    def taux_a(self, jour):
        """Taux à une date donnée (None si la date est absente)."""
        return dict(zip(self.dates, self.taux)).get(jour)

    def __len__(self):
        return len(self.taux)

    def __repr__(self):
        return f"SerieTaux({self.devise!r}, {len(self)} points, moyenne={self.moyenne():.4f})"


# ---- B.2 Piège de la liste mutable en attribut de classe -----------
class SerieMalEcrite:
    taux = []  # DANGER : la même liste est partagée par toutes les instances

    def __init__(self, devise):
        self.devise = devise

    def ajouter(self, t):
        self.taux.append(t)


class SerieBienEcrite:
    def __init__(self, devise):
        self.devise = devise
        self.taux = []  # une liste PAR instance

    def ajouter(self, t):
        self.taux.append(t)


# ---- B.3 Dataclass -------------------------------------------------
@dataclass
class SerieTauxDC:
    """Même idée que SerieTaux, mais __init__ et __repr__ sont générés."""

    devise: str
    dates: list = field(default_factory=list)  # jamais [] directement !
    taux: list = field(default_factory=list)

    def moyenne(self):
        return sum(self.taux) / len(self.taux)

    def variations(self):
        return [(b - a) / a * 100 for a, b in zip(self.taux, self.taux[1:])]


def partie_b(devise1, dates1, taux1, devise2, dates2, taux2):
    print("=== PARTIE B - Classes ===")

    # B.1 : une instance
    s1 = SerieTaux(devise1, dates1, taux1)
    print(s1)
    print(f"  Moyenne {devise1} : {s1.moyenne():.4f}")
    jour = dates1[min(5, len(dates1) - 1)]
    print(f"  Taux {devise1} au {jour} : {s1.taux_a(jour)}")

    # B.2 : plusieurs instances
    s2 = SerieTaux(devise2, dates2, taux2)
    print(s2)
    print(f"  Attribut de classe : {s1.devise_base} / {s2.devise_base}")
    print(f"  Attributs d'instance différents : {s1.devise} / {s2.devise}")

    # Le piège de la liste mutable partagée
    a, b = SerieMalEcrite(devise1), SerieMalEcrite(devise2)
    a.ajouter(taux1[0])
    print(f"  Piège : b.taux = {b.taux} (alors qu'on n'a rien ajouté à b !)")
    c, d = SerieBienEcrite(devise1), SerieBienEcrite(devise2)
    c.ajouter(taux1[0])
    print(f"  Correct : d.taux = {d.taux}")

    # B.3 : dataclass
    s1_dc = SerieTauxDC(devise1, list(dates1), list(taux1))
    print(f"  Dataclass : {s1_dc.devise}, moyenne = {s1_dc.moyenne():.4f}")
    print(f"  Égalité automatique : {SerieTauxDC('X', [], []) == SerieTauxDC('X', [], [])}")
    print()
    return s1, s2


# ======================================================================
# PARTIE C - matplotlib
# ======================================================================
def tracer_courbe(serie, chemin):
    """C.1 : évolution d'une devise (date -> taux)."""
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(serie.dates, serie.taux, color="tab:blue", linewidth=1.5)
    ax.set_title(f"Évolution du taux {serie.devise_base}/{serie.devise}")
    ax.set_xlabel("Date")
    ax.set_ylabel(f"Taux ({serie.devise} pour 1 {serie.devise_base})")
    ax.grid(alpha=0.3)
    fig.autofmt_xdate()  # dates inclinées pour rester lisibles
    fig.tight_layout()
    chemin.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(chemin, dpi=150)  # sauvegarde en PNG
    plt.close(fig)
    return chemin


def tracer_comparaison(series, chemin):
    """C.2 : comparaison (base 100), histogramme des variations, subplots."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))

    # Gauche : les devises sur un même graphique, en base 100 (comparables)
    for s in series:
        ax1.plot(s.dates, [t / s.taux[0] * 100 for t in s.taux], label=s.devise)
    ax1.set_title("Comparaison des devises (base 100)")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Indice (base 100 = premier jour)")
    ax1.legend()
    ax1.grid(alpha=0.3)
    ax1.tick_params(axis="x", rotation=45)

    # Droite : histogramme des variations quotidiennes
    for s in series:
        ax2.hist(s.variations(), bins=15, alpha=0.6, label=s.devise)
    ax2.set_title("Distribution des variations quotidiennes")
    ax2.set_xlabel("Variation (%)")
    ax2.set_ylabel("Nombre de jours")
    ax2.legend()

    fig.tight_layout()
    chemin.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(chemin, dpi=150)
    plt.close(fig)
    return chemin


def partie_c(s1, s2):
    print("=== PARTIE C - matplotlib ===")
    p1 = tracer_courbe(s1, DOSSIER_FIGURES / f"courbe_{s1.devise}.png")
    p2 = tracer_comparaison([s1, s2], DOSSIER_FIGURES / "comparaison.png")
    print(f"  Figures sauvegardées : {p1}, {p2}")
    print()


# ======================================================================
# PARTIE D - Ligne de commande (argparse)
# Dans le dépôt : ce bloc irait dans src/cli.py, les classes dans
# src/modeles.py, les graphiques dans src/graphiques.py.
# ======================================================================
def configurer_logging():
    DOSSIER_LOGS.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=DOSSIER_LOGS / "api_frankfurter.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        encoding="utf-8",
    )


def telecharger(url):
    """Appelle l'API, renvoie le dictionnaire JSON ou None en cas d'erreur (cf. B.1 / B.2)."""
    logging.info("Appel de l'API : %s", url)
    try:
        with urllib.request.urlopen(url, timeout=10) as reponse:
            brut = reponse.read().decode("utf-8")
    except urllib.error.HTTPError as erreur:  # avant URLError (sous-classe)
        logging.error("Erreur HTTP %s en appelant %s", erreur.code, url)
        print(f"Erreur : le serveur a répondu avec le code {erreur.code}.")
        return None
    except urllib.error.URLError as erreur:
        logging.error("Impossible de joindre le serveur (%s) : %s", url, erreur.reason)
        print("Erreur : impossible de joindre le serveur (vérifiez la connexion).")
        return None
    try:
        return json.loads(brut)
    except json.JSONDecodeError:
        logging.error("Réponse illisible (JSON invalide) pour %s", url)
        print("Erreur : la réponse du serveur est illisible.")
        return None


def chemin_csv(devise):
    return DOSSIER_DATA / f"taux_{BASE}_{devise}.csv"


def extraire_devise(devise):
    """Télécharge la série BASE -> devise et l'écrit en CSV. Renvoie le chemin, ou None."""
    url = f"{API}/{DEBUT}..{FIN}?from={BASE}&to={devise}"
    donnees = telecharger(url)
    if donnees is None:
        logging.warning("Série %s indisponible : étape abandonnée.", devise)
        return None

    rates = donnees.get("rates", {})
    if not rates:
        logging.warning("La réponse ne contient aucun taux pour %s.", devise)
    dates = sorted(rates)

    DOSSIER_DATA.mkdir(exist_ok=True)
    chemin = chemin_csv(devise)
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", devise])
        w.writerows((d, rates[d][devise]) for d in dates)

    logging.info("Série %s enregistrée : %d jours.", devise, len(dates))
    return chemin


def charger_serie(devise):
    """Lit donnees/taux_EUR_<devise>.csv et renvoie un objet SerieTaux."""
    chemin = chemin_csv(devise)
    if not chemin.exists():
        raise SystemExit(f"Fichier introuvable : {chemin}. Lancez d'abord 'extraire'.")
    dates, taux = [], []
    with open(chemin, newline="", encoding="utf-8") as f:
        lecteur = csv.reader(f)
        next(lecteur)  # en-tête
        for ligne in lecteur:
            if not ligne:  # ignore les lignes vides
                continue
            dates.append(date.fromisoformat(ligne[0]))
            taux.append(float(ligne[-1]))  # le taux est la dernière colonne (cf. A.1)
    return SerieTaux(devise, dates, taux)


def cmd_extraire(args):
    for devise in args.devises:
        chemin = extraire_devise(devise)
        print(f"{devise} : {chemin if chemin else 'échec (voir logs/api_frankfurter.log)'}")


def cmd_analyser(args):
    s = charger_serie(args.devise)
    v = s.variations()
    print(f"Devise      : {s.devise}")
    print(f"Période     : {s.dates[0]} -> {s.dates[-1]} ({len(s)} points)")
    print(f"Moyenne     : {s.moyenne():.4f}")
    print(f"Min / Max   : {min(s.taux):.4f} / {max(s.taux):.4f}")
    print(f"Var. moy.   : {sum(v) / len(v):+.3f} %")
    print(f"Var. max    : {max(v):+.2f} % ; min : {min(v):+.2f} %")


def cmd_graphiques(args):
    series = [charger_serie(d) for d in args.devises]
    for s in series:
        print(tracer_courbe(s, DOSSIER_FIGURES / f"courbe_{s.devise}.png"))
    if len(series) >= 2:
        print(tracer_comparaison(series, DOSSIER_FIGURES / "comparaison.png"))


def cmd_demo(args):
    s1, s2 = (charger_serie(d) for d in DEVISES_GROUPE[:2])
    partie_a(s1.dates, s1.taux)
    s1, s2 = partie_b(s1.devise, s1.dates, s1.taux, s2.devise, s2.dates, s2.taux)
    partie_c(s1, s2)


def construire_parser():
    parser = argparse.ArgumentParser(
        description="Outil d'analyse de taux de change (projet Python BFA1)."
    )
    sous = parser.add_subparsers(dest="commande", required=True)

    p = sous.add_parser("extraire", help="télécharger les taux (API Frankfurter) et les enregistrer en CSV")
    p.add_argument("--devises", nargs="+", default=DEVISES_GROUPE)
    p.set_defaults(func=cmd_extraire)

    p = sous.add_parser("analyser", help="statistiques descriptives d'une devise")
    p.add_argument("--devise", default=DEVISES_GROUPE[0])
    p.set_defaults(func=cmd_analyser)

    p = sous.add_parser("graphiques", help="produire les graphiques PNG")
    p.add_argument("--devises", nargs="+", default=DEVISES_GROUPE)
    p.set_defaults(func=cmd_graphiques)

    p = sous.add_parser("demo", help="démonstration des parties A, B et C")
    p.set_defaults(func=cmd_demo)

    return parser


def main():
    configurer_logging()
    args = construire_parser().parse_args()
    args.func(args)


# Ne s'exécute que si le fichier est lancé directement (pas s'il est importé)
if __name__ == "__main__":
    main()
