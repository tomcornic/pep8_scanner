# Architecture — Pep8_Scanner

## Analyse du code source
 - Le module natif `ast` est utilisé pour l'analyse structurelle (nommage, imports, docstrings).
 - Le module natif `tokenize` est utilisé pour les écarts purement formels non visibles dans l'AST (espacement, longueur de ligne, indentation).

## Extensibilité des règles
 - Chaque règle est une classe respectant une interface commune (`BaseRule`, avec une méthode `check()`).
 - Un registre central (`registry.py`) découvre et charge les règles disponibles.
 - Les règles sont regroupées par "profil de normes" (ex: PEP 8, PEP 257), ce qui permet d'ajouter une nouvelle norme ou un nouveau langage sans modifier le moteur d'analyse.

## Configuration
 - Format JSON.
 - Permet d'ignorer certaines règles ou d'ajuster leurs poids de gravité.

## Interface utilisateur
 - Application desktop (Tkinter/PyQt), 100% locale.
 - Sélecteur de dossier natif (browse dialog) pour choisir le projet à scanner sur la machine, sans transmission des fichiers hors de la machine.

## Structure des dossiers (src-layout)

```
pep8_scanner/
├── src/pep8_scanner/
│   ├── core/
│   │   ├── scanner.py       # parcours récursif du dossier projet
│   │   ├── analyzer.py      # orchestre ast + tokenize par fichier
│   │   └── config.py        # chargement/validation du config.json
│   ├── rules/
│   │   ├── base.py          # interface commune BaseRule (méthode check())
│   │   ├── registry.py      # registre des règles + notion de "profil de normes"
│   │   ├── pep8/            # une classe de règle par écart (indentation, espaces, nommage, imports, longueur de ligne, lignes vides...)
│   │   └── pep257/          # règles docstrings
│   ├── scoring/
│   │   └── grader.py        # somme pondérée des infractions -> note A-Z
│   ├── report/
│   │   └── explanations.py  # texte explicatif + correctif pré-écrit par règle
│   └── ui/
│       ├── app.py           # point d'entrée Tkinter/PyQt
│       └── views/           # sélecteur de dossier (browse), vue rapport
├── tests/
│   ├── rules/                # 1 test par règle (cas conforme / cas en infraction)
│   └── fixtures/              # fichiers .py d'exemple
├── config/default_config.json
└── pyproject.toml
```

## Points clés
 - **Évolutivité** : ajouter une nouvelle norme ou un nouveau langage = ajouter un nouveau dossier de règles + un profil, sans toucher au moteur (`core/`).
 - **Confidentialité** : aucun appel réseau, aucun envoi de code hors de la machine locale, conformément au cahier des charges.
