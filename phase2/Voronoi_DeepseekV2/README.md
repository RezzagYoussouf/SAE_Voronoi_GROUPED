# Diagramme de Voronoï – Application Python

Application en ligne de commande pour générer le diagramme de Voronoï à partir d’un fichier de points 2D.  
Développée dans le cadre de la SAÉ S6 – BUT Informatique.

## Résumé de la solution

Application Python en ligne de commande (CLI) qui :

1.  **Lit** un fichier texte contenant une liste de points 2D (format `x,y` par ligne) en gérant les erreurs (lignes vides, format invalide, doublons) via le module `parser.py`.
2.  **Calcule** le diagramme de Voronoï correspondant grâce à `scipy.spatial.Voronoi` dans `calculator.py`.
3.  **Visualise** le diagramme avec `matplotlib` : affichage des cellules colorées (une couleur par point), des points générateurs (en rouge) et de leurs étiquettes (A, B, C...). Le rendu est assuré par `renderer.py` avec support du zoom/pan interactif.
4.  **Exporte** le résultat aux formats PNG et SVG dans un dossier `output/` dédié, via la fonction `save_figure` de `renderer.py`.

**Choix technologiques** :
| Bibliothèque | Justification |
| :--- | :--- |
| `scipy.spatial.Voronoi` | Algorithme robuste, implémentation standard, testé et fiable. |
| `matplotlib` | Rendu de qualité, export PNG/SVG natif, interactivité (zoom/pan), testable avec backend `Agg`. |
| `pytest` / `pytest-cov` | Framework de test standard, respect du pattern AAA, couverture de code intégrée. |
| `argparse` | Interface CLI simple, sans dépendances externes (stdlib). |

## Prérequis

- Python 3.9 ou supérieur
- `pip` (gestionnaire de paquets)

## Installation

1. **Cloner ou télécharger** le projet.

2. **Créer un environnement virtuel** (recommandé) :
   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement :**

* **Sur Windows (PowerShell) :** `.\venv\Scripts\Activate`
* **Sur macOS/Linux :** `source venv/bin/activate`


4. **Installer les dépendances :**

```bash
pip install -r requirements.txt
```

### Utilisation

Lancez le script principal `main.py` en lui passant un fichier de points :

```bash
python main.py data/points.txt
```

**Options disponibles :**

* `--output <nom>` : nom de base du fichier de sortie (sans extension). Par défaut : `voronoi_output` .
* `--format <png|svg>` : format d'export (png ou svg). Par défaut : `png` .
* `--noshow` : empêche l'affichage de la fenêtre (utile pour l'export seul).

Les fichiers exportés sont enregistrés dans le dossier `output/` (créé automatiquement).

**Exemples :**

```bash
# Afficher le diagramme
python main.py data/points.txt

# Exporter en PNG sans afficher
python main.py data/points.txt --output mon_diag --format png --noshow

# Exporter en SVG
python main.py data/points.txt --output mon_diag --format svg --noshow
```

### Tests

Pour exécuter la suite de tests unitaires :

```bash
python -m pytest tests/
```

Pour plus de détails :

```bash
python -m pytest tests/ -v
```


### Couverture de code

Pour mesurer la couverture et obtenir un rapport dans la console :

```bash
python -m pytest --cov=src tests/
```

Pour générer un rapport HTML détaillé (dans le dossier `htmlcov/`) :

```bash
python -m pytest --cov=src --cov-report=html tests/
```

Ouvrez ensuite `htmlcov/index.html` dans votre navigateur.

### Structure du projet

```text
.
├── main.py                  # Point d'entrée
├── requirements.txt         # Dépendances
├── README.md                # Ce fichier
├── data/
│   └── points.txt           # Exemple de fichier de points
├── output/                  # Dossier des exports (créé automatiquement)
├── src/
│   ├── __init__.py
│   ├── models.py            # Classes Point, VoronoiResult, exceptions
│   ├── parser.py            # Lecture et validation du fichier
│   ├── calculator.py        # Calcul du diagramme (scipy)
│   ├── renderer.py          # Rendu et export (matplotlib)
│   └── cli.py               # Interface en ligne de commande
└── tests/
    ├── __init__.py
    ├── test_calculator.py
    ├── test_cli.py
    ├── test_models.py
    ├── test_parser.py
    └── test_renderer.py
```

### Checklist finale

✅ Lecture fichier points  

✅ Calcul Voronoï  

✅ Visualisation (cellules colorées, points, étiquettes, zoom/pan)  

✅ Export SVG  

✅ Export image (PNG)  

✅ TDD respecté (tests écrits en parallèle)  

✅ AAA respecté  

✅ Nommage Should/Given/When respecté  

✅ SOLID appliqué  

✅ KISS respecté  

✅ Anti-patterns évités  

✅ Couverture >97% (commande fournie)  

✅ Instructions complètes