# Voronoi App (Phase 2 — production IA)

Application Python en ligne de commande pour :
- lire un fichier texte contenant des points 2D (`x,y` par ligne),
- calculer le diagramme de Voronoï associé,
- afficher un rendu avec Matplotlib (optionnel),
- exporter en SVG (obligatoire) et PNG (optionnel).

Le choix d’une CLI (plutôt qu’une GUI) est volontaire : c’est simple à exécuter sur une machine d’étudiant, facile à tester (TDD/AAA), et pratique pour automatiser des exports.

---

## Sommaire

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Format du fichier de points](#format-du-fichier-de-points)
- [Utilisation (CLI)](#utilisation-cli)
- [Exemples](#exemples)
- [Tests](#tests)
- [Couverture de code](#couverture-de-code)
- [Erreurs fréquentes](#erreurs-fréquentes)
- [Structure du projet](#structure-du-projet)
- [Choix techniques](#choix-techniques)

---

## Prérequis

- Ubuntu (ou équivalent Linux)
- Python 3.11+ (Python 3.12 compatible)
- `python3-venv` installé

---

## Installation

Depuis la racine du projet :

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
pip install -r requirements.txt
```

Remarque : `pip install -e .` installe le package en mode éditable pour que `voronoi_app` soit importable par l’application et les tests.

---

## Format du fichier de points

Le fichier d’entrée est un fichier texte avec une paire de coordonnées par ligne :

```txt
2,4
5.3,4.5
18,29
12.5,23.7
```

Règles :

- séparateur : virgule
- espaces tolérés (`" 2 , 4 " fonctionne)
- chaque ligne doit contenir exactement 2 valeurs numériques
- doublons interdits
- au moins 4 points sont requis (contrainte SciPy/Qhull pour un Voronoï 2D)

---

## Utilisation (CLI)

Commande générale :

```bash
python -m voronoi_app.cli --input <fichier_points> [--svg <sortie.svg>] [--png <sortie.png>] [--show] [--bounds=<minx,miny,maxx,maxy>] [--padding <valeur>] [--no-axes]
```

Options :

- `--input` (obligatoire) : chemin vers le fichier de points
- `--svg` : chemin du fichier SVG de sortie
- `--png` : chemin du fichier PNG de sortie
- `--show` : affiche la figure Matplotlib à l’écran
- `--bounds=<minx,miny,maxx,maxy>` : impose un cadre d’affichage (utile pour obtenir un rendu “borné” stable)
- `--padding` : marge ajoutée autour des points si `--bounds` n’est pas fourni
- `--no-axes` : masque les axes pour un rendu plus “propre”

---

## Exemples

### 1) Export SVG + PNG (sans affichage)

```bash
python -m voronoi_app.cli --input points.txt --svg out.svg --png out.png
```

### 2) Affichage à l’écran + export

```bash
python -m voronoi_app.cli --input points.txt --svg out.svg --png out.png --show
```

### 3) Rendu borné (recommandé pour un rendu plus lisible)

```bash
python -m voronoi_app.cli --input points.txt --svg out.svg --png out.png --bounds=-5,-5,30,40
```

### 4) Sans axes (style “graphique”)

```bash
python -m voronoi_app.cli --input points.txt --svg out.svg --png out.png --no-axes
```

---

## Tests

Lancer tous les tests :

```bash
pytest
```

Les tests respectent :

- le pattern Arrange / Act / Assert (AAA),
- une convention de nommage : `Should_<ExpectedResult>_Given_<Context>_When_<Action>`.

---

## Couverture de code

Générer un rapport de couverture (console + HTML) :

```bash
pytest --cov=voronoi_app --cov-report=term-missing --cov-report=html
```

Le rapport HTML est généré dans `htmlcov/` (ouvrir `htmlcov/index.html`).

---

## Erreurs fréquentes

### “at least 4 points are required…"

SciPy/Qhull exige au minimum 4 points pour construire un Voronoï 2D dans ce contexte. Ajoutez des points (minimum 4) dans le fichier.

### Fichier invalide (ligne vide / format incorrect / non numérique)

Le parser renvoie une erreur explicite avec :

- le nom du fichier (ou `<text>`),
- le numéro de ligne,
- la cause (ligne vide, format, non numérique, doublon).

### `--bounds` ne marche pas si on met un espace

Utiliser la forme :

```bash
--bounds=-5,-5,30,40
```

(et pas `--bounds -5,-5,30,40` si votre shell/argparse l’interprète mal).

---

## Structure du projet

```txt
voronoi_app/
├── pyproject.toml
├── requirements.txt
├── README.md
├── src/
│   └── voronoi_app/
│       ├── __init__.py
│       ├── cli.py
│       ├── application/
│       │   └── voronoi_service.py
│       ├── domain/
│       │   ├── errors.py
│       │   └── models.py
│       ├── infrastructure/
│       │   ├── parsing.py
│       │   ├── export_svg.py
│       │   └── plotter.py
│       └── utils/
│           └── geometry.py
└── tests/
    └── (tests unitaires + tests d’erreurs I/O)
```

---

## Choix techniques

- Calcul Voronoï : `scipy.spatial.Voronoi` (robuste et standard)
- Rendu et export PNG : `matplotlib`
- Export SVG : génération de SVG simple et contrôlée
- Tests : `pytest` + `pytest-cov`

Ces choix privilégient :

- la facilité d’installation,
- la reproductibilité,
- la testabilité,
- la maintenabilité (structure en modules, responsabilités séparées).