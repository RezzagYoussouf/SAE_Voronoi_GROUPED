# Générateur de Diagrammes de Voronoï - Phase 2 (Généré par IA)

Ce projet répond au cahier des charges de la Phase 2 de la SAÉ S6 (BUT3 Informatique, spécialité Développement d'Applications). Il a été intégralement généré par une IA en respectant les contraintes strictes demandées : TDD, principes SOLID, Clean Code, nommage explicite et tests unitaires complets.

---

## 🎯 Objectif du projet

L'application permet de :

1.  **Lire un fichier texte** contenant une liste de points 2D (coordonnées x,y séparées par une virgule).
2.  **Calculer le diagramme de Voronoï** correspondant à cet ensemble de points.
3.  **Visualiser le résultat** via une interface graphique interactive (permettant le zoom et le déplacement).
4.  **Exporter le diagramme** dans des formats de qualité (SVG et PNG).

### 🛠️ Choix technologiques et justifcations

- **Langage :** Python. Parfait pour se concentrer sur l'algorithmique et le Clean Code sans boilerplate inutile. Il respecte le principe **KISS** (Keep It Simple, Stupid).
- **Calcul mathématique :** `scipy.spatial` (Voronoi). Robustesse assurée. Évite de recoder un algorithme complexe et potentiellement instable, tout en s'exécutant instantanément.
- **Affichage et export :** `matplotlib`. Très complet, gère nativement le rendu interactif et les exports vectoriels/matriciels avec très peu de lignes de code.
- **Tests :** `pytest` et `pytest-cov`. Standards incontestés en Python pour la rédaction de tests expressifs et le calcul de la couverture.
- **Interface :** CLI (Ligne de commande). Facilement testable, automatisable, sans la lourdeur et les bugs potentiels d'une interface graphique lourde (Tkinter/PyQt).

---

## 📁 Architecture du Projet (SOLID & Clean Code)

Le projet suit une architecture modulaire claire, empêchant le code "spaghetti", l'anti-pattern "God Class" et les dépendances circulaires.

```text
phase2_Gemini/
├── src/
│   ├── domain/               # Logique métier pure, 0 dépendance externe.
│   │   ├── exceptions.py     # Gestion explicite des erreurs.
│   │   └── models.py         # Modèles de données immuables (Point2D).
│   ├── io/                   # Interactions entrées/sorties.
│   │   └── parser.py         # Lecture et stricte validation du CSV.
│   ├── core/                 # Cœur applicatif (Services).
│   │   └── calculator.py     # Fait le pont avec les algorithmes SciPy.
│   └── presentation/         # Affichage à l'utilisateur.
│       └── renderer.py       # Utilisation isolée de matplotlib.
├── tests/                    # Tests unitaires écrits en TDD.
│   ├── test_parser.py
│   ├── test_calculator.py
│   └── test_renderer.py
├── main.py                   # Point d'entrée, gère l'injection des dépendances (DI).
├── requirements.txt          # Dépendances Python.
├── sample.txt                # Fichier exemple fourni avec le projet.
└── .coveragerc               # Omission des fichiers uniquement visuels pour la couverture.
```

### Qualité du code

- **TDD respecté :** Les modules ont été réfléchis pour être testables de manière isolée sans interaction avec les autres.
- **Modèle AAA :** Tous les tests suivent la structure visuelle `Arrange` / `Act` / `Assert`.
- **Nommage :** Tests écrits sous le format `test_Should_<ExpectedResult>_Given_<Context>_When_<Action>`.
- **Pas de Magic Numbers :** Les données comme la virgule `,` ou le nombre minimum de points requis sont des constantes figées dans la classe cible (`CsvPointParser`).
- **S.O.L.I.D. appliqué :**
  - _Single Responsibility (S) :_ Chaque fichier ne gère qu'un aspect. `io/parser.py` ne calcule rien, il s'assure juste de transformer un fichier brut en liste de la classe `Point2D`.
  - _Dependency Inversion (D) :_ `main.py` instancie et injecte les modules nécessaires, les modules ne s'auto-instancient pas sauvagement entre eux.

---

## 🚀 Installation & Exécution

**Prérequis :**
Avoir **Python 3.9** (ou supérieur) d'installé.

**1. Installation des dépendances :**
Placez-vous dans le répertoire `phase2_Gemini` et tapez la commande suivante :

```bash
pip install -r requirements.txt
```

**2. Utilisation du programme :**

L'application passe par la ligne de commande.

- **Affichage interactif seul** (ouvre une fenêtre zoomable) :

  ```bash
  python main.py sample.txt
  ```

- **Export en fichiers (SVG et PNG) de manière silencieuse :**
  ```bash
  python main.py sample.txt --export-svg diagramme.svg --export-png image.png --no-gui
  ```

---

## 🧪 Tests & Couverture

La couverture s'approche de **100 %**.
_(La classe de rendu graphique `renderer.py` a été exclue de la couverture car elle ouvre physiquement des fenêtres bloquantes `plt.show()`, obligeant un clic utilisateur, ce qui n'est pas le but de tests unitaires automatiques)._

**Lancer les tests complets (mode verbeux) :**

```bash
pytest -v tests/
```

**Générer le rapport de couverture exact :**

```bash
pytest --cov=src --cov-report=term-missing tests/
```

---

## 🛑 Limitations connues & Pistes d'amélioration

- **Jeux de données massifs :** Actuellement le parsing du fichier se fait totalement en mémoire RAM (via `f.readlines()`). Si l'utilisateur passait un fichier CSV de 10 millions de points, cela crasherait. L'alternative à envisager serait des itérateurs (`yield`) ou de réintégrer une passe `pandas` optimisée.
- **Points alignés ou superposés :** La librairie `scipy/Qhull` ne peut mathématiquement pas calculer de diagramme si vos points sont strictement coplanaires ou forment des schémas géométriques insolubles. Le code gérera cela élégamment via une erreur contrôlée (`CalculationError`), mais ne résoudra pas l'incohérence mathématique du jeu de données fourni.
