#*Pep8_Scanner*
## Ce projet a été réalisé en partie avec de l'IA générative.
## Le but de cet applicatif va être de lire un projet/ fichier en python et d'attribuer un score (de A à Z). La note A étant rservée à un code qui correspond parfaitement à la norme pep8 et inversement pour la note Z.
## L'architecture du projet resepcte les grands principes suivants : 
 - évolutif et adaptable à d'autres normes / d'autres langages.
 - la vérification du code se fera tujours en local
 - pas d'appel à l'ia dissimulé dans le code/ ni aucun envoi sur un serveur distant du code.
 - une explications des écarts (code scanné/ pep8) + propositin d'amélioration.
  

### Documents de références
Le document de référence pour la notation du fichier/ projet est le document pep 8 - style guide for Python Code, écrit par Guido van Rossum.
lien : https://peps.python.org/pep-0008/.

Le document PEP 257 - Docstring Conventions est utilisé en complément pour la vérification des docstrings.
lien : https://peps.python.org/pep-0257/.

La nomenclature des codes d'erreur `pycodestyle` (E1xx à W6xx) est utilisée comme checklist de couverture des règles, sans que la librairie soit utilisée comme dépendance du projet.

### Définitions techniques

**Interface**
 - application desktop (Tkinter/PyQt), 100% locale, pas de serveur web exposé.

**Moteur d'analyse**
 - développé from scratch (aucune librairie de lint tierce en tant que dépendance).
 - couverture complète du PEP 8 et du PEP 257 dès la V1.

**Périmètre d'analyse**
 - scan récursif d'un projet complet (multi-fichiers), pas seulement un fichier isolé.

**Notation**
 - barème de A à Z pondéré par gravité : chaque règle possède un poids selon son impact sur la lisibilité/qualité du code.

**Suggestions d'amélioration**
 - texte explicatif et exemple de correction pré-écrits pour chaque règle (pas de génération dynamique via IA, conformément à la contrainte de confidentialité du projet).

**Personnalisation**
 - fichier de configuration permettant d'ignorer certaines règles ou d'ajuster leurs poids.

**Compatibilité**
 - scanner et code analysé compatibles Python 3.6+.

**Tests**
 - suite de tests unitaires par règle (un cas conforme et un cas en infraction au minimum par règle).

**Livrable**
 - exécutable packagé (ex: PyInstaller), utilisable sans environnement Python configuré.