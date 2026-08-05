# Catalogue des règles — PEP 8 / PEP 257

Chaque règle est identifiée par un code repris de la nomenclature `pycodestyle` (E1xx-W6xx) pour PEP 8, et `pydocstyle` (D1xx-D4xx) pour PEP 257 — utilisés ici comme identifiants de référence uniquement (voir `readme.md`, aucune dépendance à ces librairies).

Palier de gravité : voir `NOTATION.md` pour les poids (Mineur=1, Modéré=2, Majeur=4, Critique=8).

Ce catalogue couvre les règles les plus significatives de chaque section du PEP 8/257. Les variantes fines (ex: sous-cas d'indentation de ligne de continuation) seront complétées au fil de l'implémentation, chacune accompagnée de son test unitaire dédié (cf. `ARCHITECTURE.md`).

## 1. Indentation

| Code | Règle | Palier |
|---|---|---|
| E101 | Mélange de tabulations et d'espaces | Critique |
| W191 | Indentation contenant des tabulations | Critique |
| E111 | Indentation non multiple de 4 | Majeur |
| E112 | Bloc indenté attendu mais absent | Majeur |
| E113 | Indentation inattendue | Majeur |
| E117 | Sur-indentation | Modéré |
| E121–E131 | Indentation incorrecte de ligne de continuation | Modéré |

## 2. Espacement

| Code | Règle | Palier |
|---|---|---|
| E201 | Espace après `(`, `[`, `{` | Mineur |
| E202 | Espace avant `)`, `]`, `}` | Mineur |
| E203 | Espace avant `:`, `,`, `;` | Mineur |
| E211 | Espace avant parenthèse/crochet d'appel | Mineur |
| E221–E224 | Espaces multiples avant/après un opérateur | Mineur |
| E225 | Espace manquant autour d'un opérateur | Modéré |
| E226 | Espace manquant autour d'un opérateur arithmétique | Mineur |
| E227 | Espace manquant autour d'un opérateur bit à bit/décalage | Modéré |
| E228 | Espace manquant autour du modulo | Modéré |
| E231 | Espace manquant après une virgule | Mineur |
| E251 | Espace inattendu autour du `=` d'un argument nommé | Mineur |
| E252 | Espace manquant autour du `=` avec annotation de type | Modéré |
| E261–E262 | Formatage incorrect d'un commentaire en fin de ligne | Mineur |
| E265–E266 | Formatage incorrect d'un commentaire de bloc | Mineur |
| E271–E275 | Espacement incorrect autour d'un mot-clé | Mineur |
| W291 | Espace en fin de ligne | Mineur |
| W293 | Espace sur une ligne vide | Mineur |

## 3. Lignes vides

| Code | Règle | Palier |
|---|---|---|
| E301 | 1 ligne vide attendue avant une méthode, absente | Modéré |
| E302 | 2 lignes vides attendues avant une fonction/classe top-level | Modéré |
| E303 | Trop de lignes vides consécutives | Mineur |
| E304 | Ligne vide après un décorateur | Modéré |
| E305 | 2 lignes vides attendues après une fonction/classe top-level | Modéré |
| E306 | 1 ligne vide attendue avant une fonction imbriquée | Modéré |
| W391 | Ligne(s) vide(s) en fin de fichier | Mineur |
| W292 | Pas de retour à la ligne en fin de fichier | Mineur |

## 4. Imports

| Code | Règle | Palier |
|---|---|---|
| E401 | Plusieurs imports sur une même ligne | Modéré |
| E402 | Import non placé en tête de module | Majeur |

## 5. Longueur de ligne

| Code | Règle | Palier |
|---|---|---|
| E501 | Ligne trop longue (> 79 caractères) | Modéré |
| E502 | Backslash redondant entre parenthèses | Mineur |
| W503/W504 | Saut de ligne avant/après un opérateur binaire | Mineur |

## 6. Instructions et bonnes pratiques

| Code | Règle | Palier |
|---|---|---|
| E701 | Instructions multiples sur une ligne (`:`) | Majeur |
| E702 | Instructions multiples sur une ligne (`;`) | Modéré |
| E703 | Point-virgule en fin d'instruction | Mineur |
| E704 | Définition de fonction sur une seule ligne | Modéré |
| E711 | Comparaison à `None` sans `is` | Majeur |
| E712 | Comparaison à `True`/`False` sans `is` | Majeur |
| E713 | Test d'appartenance sans `not in` | Modéré |
| E714 | Test d'identité sans `is not` | Modéré |
| E721 | Comparaison de types avec `==` | Majeur |
| E722 | `except:` nu (sans type d'exception) | Critique |
| E731 | Lambda assignée à une variable au lieu d'un `def` | Modéré |
| W605 | Séquence d'échappement invalide dans une chaîne | Majeur |

## 7. Noms ambigus

| Code | Règle | Palier |
|---|---|---|
| E741 | Nom de variable ambigu (`l`, `O`, `I`) | Majeur |
| E742 | Nom de classe ambigu | Majeur |
| E743 | Nom de fonction ambigu | Majeur |

## 8. Conventions de nommage

| Code | Règle | Palier |
|---|---|---|
| N801 | Nom de classe non en CapWords | Modéré |
| N802 | Nom de fonction non en snake_case | Modéré |
| N803 | Nom d'argument non en snake_case | Modéré |
| N806 | Variable locale non en snake_case | Modéré |
| N816 | Constante non en UPPER_CASE | Modéré |
| N818 | Nom d'exception ne se terminant pas par `Error` | Mineur |

## 9. Docstrings (PEP 257)

| Code | Règle | Palier |
|---|---|---|
| D100 | Docstring manquante sur un module public | Majeur |
| D101 | Docstring manquante sur une classe publique | Majeur |
| D102 | Docstring manquante sur une méthode publique | Majeur |
| D103 | Docstring manquante sur une fonction publique | Majeur |
| D105 | Docstring manquante sur une méthode magique | Mineur |
| D200 | Docstring courte ne tenant pas sur une seule ligne | Mineur |
| D201–D202 | Ligne(s) vide(s) en trop avant/après la docstring | Mineur |
| D210 | Espaces superflus en début/fin de docstring | Mineur |
| D300 | Guillemets triples doubles non utilisés | Modéré |
| D400 | Première ligne ne se terminant pas par un point | Mineur |
| D401 | Première ligne non à l'impératif | Mineur |
| D419 | Docstring vide | Majeur |

## Répartition par palier (indicatif)

| Palier | Nombre de règles |
|---|---|
| Mineur | ~28 |
| Modéré | ~24 |
| Majeur | ~16 |
| Critique | 3 |
