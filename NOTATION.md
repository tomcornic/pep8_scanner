# Notation — Pep8_Scanner

## Formule de score

**Densité pondérée** = (somme des poids des infractions) / (nombre de lignes de code / 100)

Le score est exprimé en "points d'infraction pondérés pour 100 lignes de code". Cette normalisation par la taille garantit qu'un gros fichier/projet n'est pas mécaniquement pénalisé par rapport à un petit.

## Poids par palier de gravité

| Palier | Poids | Exemples |
|---|---|---|
| Mineur | 1 | espace en trop, ligne vide superflue |
| Modéré | 2 | ligne trop longue, nommage non conforme |
| Majeur | 4 | erreur d'indentation, docstring manquante sur API publique |
| Critique | 8 | mélange tabs/espaces, erreur cassant potentiellement le code |

Chaque règle du registre se voit assigner un de ces 4 poids. Ces poids sont ajustables via le fichier de configuration JSON (voir `ARCHITECTURE.md`).

## Table de conversion score → lettre

Paliers réguliers de largeur 2, sur l'échelle des 26 lettres A à Z :

| Lettre | Densité pondérée |
|---|---|
| A | [0 – 2[ |
| B | [2 – 4[ |
| C | [4 – 6[ |
| D | [6 – 8[ |
| E | [8 – 10[ |
| F | [10 – 12[ |
| G | [12 – 14[ |
| H | [14 – 16[ |
| I | [16 – 18[ |
| J | [18 – 20[ |
| K | [20 – 22[ |
| L | [22 – 24[ |
| M | [24 – 26[ |
| N | [26 – 28[ |
| O | [28 – 30[ |
| P | [30 – 32[ |
| Q | [32 – 34[ |
| R | [34 – 36[ |
| S | [36 – 38[ |
| T | [38 – 40[ |
| U | [40 – 42[ |
| V | [42 – 44[ |
| W | [44 – 46[ |
| X | [46 – 48[ |
| Y | [48 – 50[ |
| Z | ≥ 50 |

## Agrégation multi-fichiers

La note globale d'un projet est calculée comme la moyenne des densités par fichier, pondérée par le nombre de lignes de chaque fichier, puis reconvertie en lettre via la table ci-dessus.

Cette moyenne pondérée par LOC équivaut mathématiquement à calculer directement la densité globale sur l'ensemble du projet (somme totale des poids d'infractions / LOC total du projet) — le calcul reste donc cohérent entre le niveau fichier et le niveau projet.
