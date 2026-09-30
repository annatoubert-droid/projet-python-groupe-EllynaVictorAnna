# 📘 Notes — Séance 4

**Projet Python · Python idiomatique, POO, matplotlib et finalisation**



# Bloc 1 — Python plus idiomatique

Données utilisées dans les exemples :

```python
dates = ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"]
taux = [1.0850, 1.0912, 1.0877, 1.0950]
```

## 1. C'est quoi une compréhension de liste ? Quel avantage par rapport à une boucle `for` classique ?

Une **compréhension de liste** est une syntaxe compacte qui permet de **construire une nouvelle liste** à partir d'un itérable, en une seule expression :

```python
[expression for element in iterable if condition]
```

La partie `if condition` est optionnelle : elle sert à filtrer.

**Comparaison avec une boucle classique** — calcul des variations quotidiennes en % :

```python
# Boucle for classique
variations = []
for i in range(1, len(taux)):
    variations.append((taux[i] - taux[i - 1]) / taux[i - 1] * 100)

# Compréhension de liste
variations = [(taux[i] - taux[i - 1]) / taux[i - 1] * 100
              for i in range(1, len(taux))]
```

Avec un filtre :

```python
hausses = [t for t in taux if t > 1.09]   # [1.0912, 1.0950]
```

**Compréhension de dictionnaire** (même principe, avec `{clé: valeur ...}`) :

```python
taux_par_date = {d: t for d, t in zip(dates, taux)}
# {'2026-01-01': 1.085, '2026-01-02': 1.0912, ...}
```

Il existe aussi la compréhension d'ensemble : `{x for x in iterable}`.

**Avantages :**

- ✅ **Plus concis** : pas de liste vide à créer ni de `.append()`.
- ✅ **Plus lisible** (quand l'expression reste simple) : on voit tout de suite qu'on construit une liste.
- ✅ **Plus « pythonique »** et généralement un peu **plus rapide** qu'une boucle avec `append`.
- ✅ Pas de variable temporaire qui traîne : dans Python 3, la variable de boucle reste locale à la compréhension.

**Limite :** si la logique devient complexe (plusieurs conditions imbriquées, effets de bord), une boucle `for` classique reste plus lisible.

---

## 2. À quoi servent `enumerate` et `zip` ?

### `enumerate` : obtenir l'indice **et** la valeur

Il évite d'écrire `range(len(liste))` et d'indexer à la main.

```python
for i, t in enumerate(taux):
    print(i, t)
# 0 1.085
# 1 1.0912
# ...

for i, t in enumerate(taux, start=1):   # démarrer à 1 au lieu de 0
    print(f"Jour {i} : {t}")
```

### `zip` : parcourir **plusieurs séquences en parallèle**

Il associe les éléments de même position sous forme de tuples.

```python
for d, t in zip(dates, taux):
    print(d, t)
# 2026-01-01 1.085
# 2026-01-02 1.0912
# ...

taux_par_date = dict(zip(dates, taux))   # construire un dictionnaire
```

⚠️ `zip` **s'arrête à la séquence la plus courte** : si les deux listes n'ont pas la même longueur, les éléments en trop sont ignorés silencieusement (on peut utiliser `zip(..., strict=True)` en Python ≥ 3.10 pour lever une erreur dans ce cas).

---

## 3. Comment trier une liste selon un critère (`sorted` avec `key`) ?

`sorted(iterable, key=fonction, reverse=False)` **renvoie une nouvelle liste triée**. L'argument `key` est une **fonction appliquée à chaque élément** : le tri se fait sur la valeur qu'elle renvoie.

```python
observations = list(zip(dates, taux))
# [('2026-01-01', 1.085), ('2026-01-02', 1.0912), ...]

# Trier par taux croissant (critère : le 2e élément du tuple)
par_taux = sorted(observations, key=lambda obs: obs[1])

# Trier par taux décroissant
par_taux_desc = sorted(observations, key=lambda obs: obs[1], reverse=True)

# Autres exemples
sorted(["EUR", "usd", "GBP"], key=str.lower)      # tri insensible à la casse
sorted(["EUR", "USD", "CHF"], key=len)            # tri par longueur
```

**À retenir :**

- `sorted()` **ne modifie pas** la liste d'origine, alors que `liste.sort()` la trie **en place** (et renvoie `None`).
- `reverse=True` inverse l'ordre.
- Le tri est **stable** : deux éléments à égalité gardent leur ordre relatif.
- Alternative à la lambda : `operator.itemgetter(1)`.

---

## 4. C'est quoi une f-string ? Comment afficher un nombre à deux décimales ?

Une **f-string** (*formatted string literal*, Python ≥ 3.6) est une chaîne préfixée par `f` dans laquelle on peut insérer directement des **variables ou des expressions** entre accolades `{}`.

```python
devise = "USD"
taux_usd = 1.08765

print(f"Le taux {devise} vaut {taux_usd}")
# Le taux USD vaut 1.08765
```

**Afficher deux décimales** avec le spécificateur de format `:.2f` :

```python
print(f"Taux : {taux_usd:.2f}")      # Taux : 1.09
```

**Autres formats utiles :**

```python
from datetime import date

f"{1234567.891:,.2f}"        # '1,234,567.89'   séparateur de milliers
f"{0.0523:.1%}"              # '5.2%'           pourcentage
f"{taux_usd:8.3f}"           # '   1.088'       largeur 8, 3 décimales
f"{'EUR':>10}"               # '       EUR'     aligné à droite sur 10 caractères
f"{date(2026, 1, 15):%d/%m/%Y}"   # '15/01/2026' formatage de date
f"{2 + 3 = }"                # '2 + 3 = 5'      (mode debug, Python ≥ 3.8)
```

**Avantages** par rapport à `%` et `.format()` : plus lisible, plus court, et plus rapide.

---

## 5. C'est quoi une fonction lambda ?

Une **fonction lambda** est une **petite fonction anonyme** (sans nom), définie en une seule ligne avec le mot-clé `lambda` :

```python
lambda arguments: expression
```

Elle **renvoie automatiquement la valeur de l'expression**, sans `return`.

```python
carre = lambda x: x ** 2        # équivalent à : def carre(x): return x ** 2
carre(4)                        # 16
```

Elle est surtout utile pour passer **une fonction simple en argument**, à usage unique : `sorted(key=...)`, `map`, `filter`…

```python
# map : appliquer une fonction à chaque élément
en_pourcent = list(map(lambda t: t * 100, taux))

# filter : ne garder que les éléments qui vérifient une condition
eleves = list(filter(lambda t: t > 1.09, taux))          # [1.0912, 1.095]

# key dans sorted
sorted(observations, key=lambda obs: obs[1])
```

**Remarques :**

- Une lambda ne contient **qu'une seule expression** (pas d'instructions multiples, pas d'affectation).
- `map` et `filter` renvoient des **itérateurs** : il faut les convertir avec `list(...)` pour voir le résultat.
- Souvent, une compréhension de liste est plus lisible que `map`/`filter` + lambda : `[t * 100 for t in taux]`.
- Si la fonction devient complexe ou réutilisée, il vaut mieux une vraie fonction `def`.

---

# Bloc 2 — La programmation orientée objet

Exemple fil rouge : la classe `SerieTaux`.

```python
class SerieTaux:
    """Série temporelle des taux d'une devise."""

    def __init__(self, devise, dates, taux):
        self.devise = devise
        self.dates = dates
        self.taux = taux

    def moyenne(self):
        return sum(self.taux) / len(self.taux)

    def variations(self):
        """Variations quotidiennes en %."""
        return [(self.taux[i] - self.taux[i - 1]) / self.taux[i - 1] * 100
                for i in range(1, len(self.taux))]

    def taux_a(self, date):
        """Taux à une date donnée (None si la date est absente)."""
        return dict(zip(self.dates, self.taux)).get(date)


usd = SerieTaux("USD", ["2026-01-01", "2026-01-02"], [1.0850, 1.0912])
print(usd.moyenne())               # 1.0881
print(usd.taux_a("2026-01-02"))    # 1.0912
```

## 1. C'est quoi une classe ? Un objet ? Une instance ? À quoi sert `self` ?

- **Classe** : un **modèle** (un « plan de construction ») qui décrit les **données** (attributs) et les **comportements** (méthodes) d'un type d'objet. Ici, `SerieTaux` est une classe.
- **Objet** : une **entité concrète** créée à partir d'une classe, qui contient ses propres données et peut utiliser les méthodes de la classe. Ici, `usd` est un objet.
- **Instance** : c'est **un objet vu comme l'exemplaire d'une classe donnée**. « `usd` est une instance de `SerieTaux` ». Dans le langage courant, *objet* et *instance* sont quasiment synonymes ; on dit « instance » pour insister sur le lien avec sa classe. **Instancier** = créer un objet à partir d'une classe (`SerieTaux(...)`).
- **`self`** : c'est le **premier paramètre de chaque méthode d'instance**. Il représente **l'objet courant**, celui sur lequel la méthode est appelée. Python le passe automatiquement :

```python
usd.moyenne()            # Python exécute en réalité : SerieTaux.moyenne(usd)
```

C'est grâce à `self` qu'une méthode accède aux attributs **propres à cet objet** (`self.taux`) : `usd.moyenne()` et `gbp.moyenne()` utilisent chacun leurs propres données. Le nom `self` est une convention (mais fortement respectée).

---

## 2. À quoi sert `__init__` ?

`__init__` est une **méthode spéciale** (le fameux « initialiseur ») appelée **automatiquement à la création d'une instance**, juste après que l'objet a été créé :

```python
usd = SerieTaux("USD", dates, taux)   # déclenche __init__(usd, "USD", dates, taux)
```

Son rôle est d'**initialiser l'état de l'objet** : elle reçoit les paramètres et crée les **attributs d'instance** (`self.devise = devise`, etc.), pour que l'objet soit dans un état valide dès sa création. On peut aussi y valider les données (par exemple lever une erreur si `dates` et `taux` n'ont pas la même longueur).

> Précision : `__init__` **n'a pas de `return`** (elle renvoie `None`). Techniquement, c'est `__new__` qui crée l'objet ; `__init__` ne fait que l'initialiser, d'où le nom d'« initialiseur » plutôt que de « constructeur ».

---

## 3. Différence entre un attribut de classe et un attribut d'instance ?

| | **Attribut de classe** | **Attribut d'instance** |
|---|---|---|
| **Où est-il défini ?** | Dans le corps de la classe, hors des méthodes | Dans `__init__` (ou une méthode) via `self.xxx = ...` |
| **À qui appartient-il ?** | À la **classe** : **partagé** par toutes les instances | À **chaque objet** : **propre** à l'instance |
| **Accès** | `SerieTaux.base` ou `usd.base` | `usd.devise` |
| **Usage typique** | Constantes, valeurs communes | Données propres à chaque objet |

```python
class SerieTaux:
    monnaie_base = "EUR"          # attribut de classe : commun à toutes les séries

    def __init__(self, devise, taux):
        self.devise = devise      # attributs d'instance : propres à chaque objet
        self.taux = taux

usd = SerieTaux("USD", [1.08])
gbp = SerieTaux("GBP", [0.86])

usd.monnaie_base    # 'EUR'
gbp.monnaie_base    # 'EUR'   (même valeur partagée)
usd.devise          # 'USD'
gbp.devise          # 'GBP'   (valeur propre à chaque objet)
```

### ⚠️ Le piège de la liste mutable en attribut de classe

Comme pour les dictionnaires en séance 1, un objet **mutable** (liste, dictionnaire) déclaré en attribut de classe est **partagé par toutes les instances** :

```python
class SerieTaux:
    taux = []                     # ❌ MAUVAIS : une seule liste pour tout le monde

usd = SerieTaux()
gbp = SerieTaux()
usd.taux.append(1.08)
print(gbp.taux)                   # [1.08]  ← la liste de gbp a été modifiée aussi !
```

**Solution :** créer la liste **dans `__init__`**, pour que chaque instance ait la sienne :

```python
class SerieTaux:
    def __init__(self):
        self.taux = []            # ✅ une liste distincte par instance
```

> Avec une dataclass, on utilise `field(default_factory=list)`.

---

## 4. Qu'apporte une `dataclass` par rapport à une classe écrite entièrement à la main ?

Le décorateur `@dataclass` (module `dataclasses`, Python ≥ 3.7) **génère automatiquement le code répétitif** à partir des attributs déclarés avec leurs annotations de type : `__init__`, `__repr__` et `__eq__`.

**Classe écrite à la main :**

```python
class SerieTaux:
    def __init__(self, devise, dates, taux):
        self.devise = devise
        self.dates = dates
        self.taux = taux

    def __repr__(self):
        return f"SerieTaux(devise={self.devise!r}, dates={self.dates!r}, taux={self.taux!r})"

    def __eq__(self, other):
        return (self.devise, self.dates, self.taux) == (other.devise, other.dates, other.taux)
```

**Avec une dataclass :**

```python
from dataclasses import dataclass, field

@dataclass
class SerieTaux:
    devise: str
    dates: list[str] = field(default_factory=list)   # liste mutable : default_factory obligatoire
    taux: list[float] = field(default_factory=list)

    def moyenne(self):
        return sum(self.taux) / len(self.taux)
```

**Apports :**

- ✅ **Moins de code** : plus besoin d'écrire `__init__`, `__repr__`, `__eq__`.
- ✅ **Un affichage lisible** : `print(usd)` donne `SerieTaux(devise='USD', ...)` au lieu de `<__main__.SerieTaux object at 0x...>`.
- ✅ **Comparaison** automatique des objets par leurs valeurs.
- ✅ **Code plus clair** : les attributs et leurs types sont listés d'un coup d'œil.
- ✅ **Options** : `frozen=True` (objet immuable), `order=True` (comparaison `<`, `>`), valeurs par défaut.
- ✅ **Protection contre le piège vu plus haut** : Python refuse un défaut mutable direct (`taux: list = []` lève une `ValueError`) et impose `default_factory`.

On peut toujours **ajouter ses propres méthodes** (`moyenne`, `variations`…) : une dataclass reste une classe normale.

---

# Bloc 3 — Visualiser avec matplotlib

Exemple de base :

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(dates, taux, marker="o", label="USD")
ax.set_title("Évolution du taux EUR/USD")
ax.set_xlabel("Date")
ax.set_ylabel("Taux")
ax.legend()
ax.grid(True)
fig.savefig("usd.png", dpi=150, bbox_inches="tight")
plt.close(fig)
```

## 1. Différence entre la figure et les axes ? Pourquoi préférer `fig, ax = plt.subplots()` à l'usage direct de `pyplot` ?

- La **figure** (`Figure`) est le **conteneur global** : c'est la « feuille » ou la fenêtre entière, qui sera sauvegardée en image. Elle définit la taille, la résolution (dpi), et peut contenir un ou plusieurs graphiques.
- Les **axes** (`Axes`) sont **un graphique à l'intérieur de la figure** : la zone de tracé avec ses axes x/y, ses courbes, son titre, sa légende, sa grille. **Une figure peut contenir plusieurs axes** (subplots).

> ⚠️ Ne pas confondre **`Axes`** (le graphique entier, objet sur lequel on appelle `.plot()`) et **`Axis`** (un seul axe : l'axe x ou l'axe y).

```
Figure
├── Axes 1  (ex. courbe des taux)
└── Axes 2  (ex. histogramme des variations)
```

**Pourquoi préférer `fig, ax = plt.subplots()` (interface orientée objet) :**

- ✅ **Explicite** : on sait toujours sur quel graphique on agit (`ax.plot(...)`, `ax.set_title(...)`).
- ✅ **Indispensable dès qu'il y a plusieurs graphiques** : `fig, axes = plt.subplots(1, 2)` puis `axes[0]`, `axes[1]`.
- ✅ **Pas d'« état global » caché** : l'interface `pyplot` directe (`plt.plot(...)`) agit sur la « figure courante », ce qui provoque des erreurs (tracé au mauvais endroit, superposition de figures) quand on en manipule plusieurs ou qu'on appelle des fonctions.
- ✅ **Code réutilisable** : on peut écrire des fonctions `tracer(ax, serie)` qui reçoivent un `ax`.
- ✅ **Plus de contrôle** sur la taille (`figsize`), la sauvegarde (`fig.savefig`) et la mise en page.

`pyplot` reste utile pour créer la figure (`plt.subplots()`), afficher (`plt.show()`) et fermer (`plt.close(fig)`).

---

## 2. Quel type de graphique pour quel type de donnée ?

| Type de donnée / objectif | Graphique adapté | Fonction matplotlib | Exemple dans le projet |
|---|---|---|---|
| **Série temporelle** (évolution dans le temps) | **Courbe** (ligne) | `ax.plot(dates, valeurs)` | Taux EUR/USD au fil des jours |
| **Distribution** (répartition des valeurs) | **Histogramme** (ou boîte à moustaches) | `ax.hist(valeurs, bins=...)` · `ax.boxplot(...)` | Variations quotidiennes en % |
| **Comparaison de séries** (même unité, même période) | **Plusieurs courbes sur les mêmes axes** avec légende | `ax.plot(...)` ×N + `ax.legend()` | Les 2 devises du groupe. Si les échelles diffèrent beaucoup : normaliser (base 100) ou utiliser des subplots |
| **Comparaison de catégories** | **Diagramme en barres** | `ax.bar(categories, valeurs)` | Taux moyen par devise |
| **Relation entre deux variables** | **Nuage de points** | `ax.scatter(x, y)` | Taux USD vs taux GBP |

**Règle d'or :** un bon graphique a un **titre**, des **axes légendés (avec unités)** et une **légende** dès qu'il y a plusieurs séries. On évite les barres pour une série temporelle et les courbes pour des catégories sans ordre.

---

## 3. Comment sauvegarder une figure en PNG ?

Avec la méthode `savefig` de la figure :

```python
fig.savefig("graphiques/usd.png", dpi=150, bbox_inches="tight")
```

- Le **format est déduit de l'extension** (`.png`, `.pdf`, `.svg`, `.jpg`…).
- `dpi` règle la **résolution** (150–300 pour un rapport).
- `bbox_inches="tight"` **évite que les titres ou légendes soient coupés**.
- Avec l'interface directe : `plt.savefig("usd.png")`.

**Bonnes pratiques :**

- Appeler `savefig` **avant** `plt.show()` (sinon l'image sauvegardée peut être vide après la fermeture de la fenêtre).
- Appeler `plt.close(fig)` après la sauvegarde pour **libérer la mémoire** (important quand on génère plusieurs figures dans une boucle).
- S'assurer que le dossier de destination existe (`Path("graphiques").mkdir(exist_ok=True)`).

---

# Bloc 4 — Assembler et finaliser

## 1. À quoi sert `argparse` ? Pourquoi une ligne de commande plutôt que des `input()` ?

`argparse` est le module de la bibliothèque standard qui permet de **définir et lire les arguments passés en ligne de commande** : il gère l'analyse, la conversion de types, les valeurs par défaut, la validation, les messages d'erreur, et génère automatiquement l'aide (`--help`). Il gère aussi les **sous-commandes**.

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Outil d'analyse des taux de change")
    sous = parser.add_subparsers(dest="commande", required=True)

    p_extraire = sous.add_parser("extraire", help="Télécharger les taux")
    p_extraire.add_argument("--devise", required=True, help="Code de la devise (ex. USD)")

    p_analyser = sous.add_parser("analyser", help="Calculer les statistiques")
    p_analyser.add_argument("--devise", required=True)

    p_graph = sous.add_parser("graphiques", help="Générer les PNG")
    p_graph.add_argument("--sortie", default="graphiques/", help="Dossier de sortie")

    args = parser.parse_args()
    print(args.commande)

if __name__ == "__main__":
    main()
```

Utilisation :

```bash
python -m src.cli extraire --devise USD
python -m src.cli analyser --devise USD
python -m src.cli graphiques --sortie figures/
python -m src.cli --help
```

**Pourquoi la ligne de commande plutôt que `input()` :**

- ✅ **Automatisable** : un script avec `input()` s'arrête et attend un humain ; une commande peut être lancée par un autre script, un `cron`, un pipeline ou une CI.
- ✅ **Reproductible** : la commande exacte peut être copiée dans le README et rejouée à l'identique.
- ✅ **Auto-documentée** : `--help` décrit toutes les options.
- ✅ **Validation** : types, valeurs autorisées (`choices`), arguments obligatoires, erreurs claires.
- ✅ **Plus rapide** : pas de questions répétitives à répondre à chaque exécution.
- ✅ **Testable** : facile à appeler avec différents paramètres.

---

## 2. Que fait exactement `if __name__ == "__main__"` ?

Chaque module Python possède une variable spéciale `__name__` :

- Si le fichier est **exécuté directement** (`python mon_fichier.py`), Python met `__name__ = "__main__"`.
- Si le fichier est **importé** par un autre (`import mon_fichier`), `__name__` vaut le **nom du module** (`"mon_fichier"`).

La condition `if __name__ == "__main__":` permet donc d'exécuter un bloc de code **seulement quand le fichier est lancé comme script**, et **pas** lorsqu'il est importé.

```python
# src/analyse.py
def moyenne(valeurs):
    return sum(valeurs) / len(valeurs)

if __name__ == "__main__":
    # Ne s'exécute que par : python src/analyse.py
    print(moyenne([1, 2, 3]))
```

Ainsi, on peut **réutiliser les fonctions** du fichier via `from src.analyse import moyenne` **sans déclencher** l'exécution du programme (pas d'affichage, pas de téléchargement, pas de lancement de `main()` au moment de l'import). C'est aussi la structure standard des points d'entrée (`main()`).

---

## 3. C'est quoi un module ? Un package ?

- **Module** : un **fichier `.py`** qui contient du code (fonctions, classes, variables) réutilisable via `import`. Exemple : `src/analyse.py` est le module `analyse`.
- **Package** : un **dossier regroupant plusieurs modules**, importable comme un ensemble. Il contient traditionnellement un fichier `__init__.py` (qui peut être vide et signale à Python que le dossier est un package).
- La **bibliothèque standard** (`argparse`, `datetime`, `json`…) et les bibliothèques tierces (`matplotlib`) sont des modules/packages.

Exemple d'organisation du projet :

```
projet/
├── src/                   # package : le code source
│   ├── __init__.py
│   ├── extraction.py      # module
│   ├── analyse.py         # module
│   ├── modeles.py         # module (classe SerieTaux)
│   ├── graphiques.py      # module
│   └── cli.py             # module (argparse)
├── docs/
│   └── notes_seance4.md
├── graphiques/            # PNG générés
├── README.md
├── requirements.txt
└── .gitignore
```

```python
from src.modeles import SerieTaux     # importer une classe d'un module du package
import src.analyse                    # importer un module entier
```

**Intérêt de cette organisation :** un code **structuré, réutilisable, testable** et plus facile à maintenir qu'un gros fichier unique.

---

## 4. Que doit contenir un bon README ? À quoi servent `requirements.txt` et `.gitignore` ?

### Un bon `README.md` (la « vitrine » du projet)

- **Titre et description** : ce que fait le projet et son objectif, en quelques lignes.
- **Prérequis** : version de Python, système d'exploitation éventuel.
- **Installation** : cloner le dépôt, créer l'environnement virtuel, installer les dépendances.
- **Utilisation avec des exemples de commandes** concrètes (et éventuellement leurs résultats).
- **Structure du projet** (arborescence commentée).
- **Résultats / aperçu** : graphiques principaux.
- **Auteurs**, contexte (cours, année) et licence si besoin.

Exemple d'installation à faire figurer :

```bash
git clone <url-du-depot>
cd projet
python -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

### `requirements.txt`

Fichier qui **liste les dépendances Python** du projet (avec leurs versions) pour que **n'importe qui puisse recréer le même environnement** :

```bash
pip freeze > requirements.txt      # figer les versions installées
pip install -r requirements.txt    # réinstaller les dépendances
```

Exemple de contenu :

```
matplotlib==3.9.2
requests==2.32.3
```

Cela garantit la **reproductibilité** (« ça marche chez moi » → « ça marche chez tout le monde »).

### `.gitignore`

Fichier qui indique à Git **les fichiers et dossiers à ne pas suivre ni versionner** : ceux qui sont **générés, temporaires, volumineux ou confidentiels**.

```gitignore
# Environnement virtuel
.venv/
venv/

# Fichiers générés par Python
__pycache__/
*.pyc

# Secrets et configuration locale
.env

# Fichiers d'IDE / système
.vscode/
.idea/
.DS_Store
```

Il garde le dépôt **propre et léger**, évite de committer par erreur des **secrets** (clés d'API, mots de passe), et évite les conflits inutiles entre les membres du groupe.

---

*Notes rédigées pour la séance 4 — à placer dans `docs/notes_seance4.md`, puis à commiter :*

```bash
git add docs/notes_seance4.md
git commit -m "docs: notes de la séance 4"
git push
```
