# SAÉ S6 — Diagrammes de Voronoï (BUT3 Informatique)

Ce dépôt contient notre travail pour la **SAÉ S6** sur les **diagrammes de Voronoï** : une application qui lit un fichier de points 2D, calcule le diagramme de Voronoï et permet de le visualiser, avec export possible (**SVG** et/ou image).

Le projet est organisé en **trois phases** :
- **Phase 1** : réalisation sans aucune aide d’IA.
- **Phase 2** : réalisation avec plusieurs IA génératrices de code, avec suivi des prompts et des corrections.
- **Phase 3** : rapport sans IA sur les risques liés à l’usage d’IA génératives.

---

## Membres de l’équipe (Groupe D)

- Habib Ben Mansour
- Dalla Diallo
- Iliasse Bellouch
- Marewane Fertikh
- Yannel Aissani
- Youssouf Rezzag-Mahcene

---

## Objectif du projet

À partir d’un fichier texte contenant une liste de points (une paire `x,y` par ligne), l’application doit :
- lire et valider les points,
- calculer un diagramme de Voronoï,
- afficher le résultat,
- exporter le rendu en SVG (et éventuellement en image).

Exemple de fichier d’entrée :

```txt
2,4
5.3,4.5
18,29
12.5,23.7
```

---

## Organisation du dépôt

L’organisation exacte peut varier selon les membres, mais on retrouve en général :

- `phase1/` : version développée à la main (sans IA)
- `phase2/` : versions développées avec IA (au moins 4 IA différentes)
  - journaux de prompts
  - journal de corrections / temps passé
  - code de l’application IA
- `phase3/` : rapports sur les risques (rédigés sans IA), un thème par personne

---

## Phase 1 — Développement sans IA

But : construire l’application en respectant le cahier des charges, **sans utiliser d’IA** (ni génération de code, ni assistance).

Livrables typiques :
- code source
- consignes d’utilisation (README)
- captures / exports (SVG, image)

---

## Phase 2 — Développement avec IA génératives

But : produire une application équivalente avec l’aide de plusieurs IA génératrices de code (**minimum 4**).

IA utilisées (selon notre groupe) :
- ChatGPT (OpenAI)
- Gemini
- DeepSeek
- Claude

Livrables attendus :
- le code complet de la version IA
- une série de tests (objectif : bonnes pratiques, tests automatisés)
- un journal de prompts (ce qu’on a demandé à l’IA)
- un journal de corrections (temps passé et problèmes rencontrés)

---

## Phase 3 — Rapport sur les risques (sans IA)

But : analyser les risques liés à l’usage d’IA génératives en développement logiciel. Chaque membre traite un thème différent (sans doublon dans l’équipe).

### Répartition des sujets (phase 3)

- **Habib** : conséquences sur les personnes travaillant avec l'IA
- **Dalla** : réputation et appropriation du produit par le public
- **Iliasse** : environnement
- **Marewane** : légalité et responsabilité
- **Yannel** : qualité du logiciel et de la maintenance
- **Youssouf** : souveraineté et géopolitique

---

## Comment exécuter une version

Chaque phase/version peut avoir ses propres instructions. En général :
- les instructions d’exécution et d’installation se trouvent dans le `README.md` de la phase concernée,
- la phase 2 contient aussi les commandes de tests et de couverture si elles sont demandées.

---

## Remarques

- La phase 1 sert de référence “humaine”.
- La phase 2 sert à comparer la production IA avec une version faite à la main (qualité, temps, corrections, robustesse, tests).
- La phase 3 sert à prendre du recul sur les risques, au-delà de la simple technique.