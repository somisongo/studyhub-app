# Guide de Workflow Git pour StudyHub

Ce document décrit les pratiques Git recommandées pour le projet StudyHub. Suivre ces directives permettra d'assurer une collaboration efficace et le maintien d'un historique Git propre et compréhensible.

## Structure des Branches

Le projet utilise une structure de branches basée sur GitFlow:

- `main` - Branche principale contenant le code de production
- `develop` - Branche d'intégration pour les fonctionnalités en cours de développement
- `feature/*` - Branches pour le développement de nouvelles fonctionnalités
- `bugfix/*` - Branches pour la correction de bugs
- `release/*` - Branches pour la préparation des versions de production
- `hotfix/*` - Branches pour les corrections urgentes en production

## Workflow de Développement

### 1. Commencer une nouvelle fonctionnalité

```bash
# Assurez-vous d'avoir la dernière version de develop
git checkout develop
git pull

# Créer une nouvelle branche feature
git checkout -b feature/nom-de-la-fonctionnalite

# Travailler sur votre fonctionnalité...
# Faites des commits réguliers
git add .
git commit -m "Description claire de la modification"
```

### 2. Mettre à jour votre branche avec les changements de develop

```bash
# Pendant que vous travaillez, d'autres modifications peuvent être apportées à develop
git checkout develop
git pull
git checkout feature/nom-de-la-fonctionnalite
git merge develop

# Résoudre les conflits si nécessaire, puis:
git add .
git commit -m "Merge develop into feature/nom-de-la-fonctionnalite"
```

### 3. Terminer une fonctionnalité

```bash
# Pousser votre branche vers le dépôt distant
git push -u origin feature/nom-de-la-fonctionnalite

# Créer une Pull Request via GitHub
# Attendre les revues de code et l'approbation
# Après approbation, merger dans develop
```

### 4. Correction de bugs

```bash
# Pour corriger un bug dans develop
git checkout develop
git pull
git checkout -b bugfix/description-du-bug

# Pour corriger un bug en production
git checkout main
git pull
git checkout -b hotfix/description-du-bug
```

### 5. Préparer une version

```bash
git checkout develop
git pull
git checkout -b release/v1.0.0

# Faire les derniers ajustements, mises à jour de version, etc.
# Tests finaux

# Une fois prêt:
git checkout main
git merge release/v1.0.0 --no-ff
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin main --tags

# Ne pas oublier de mettre à jour develop aussi
git checkout develop
git merge release/v1.0.0 --no-ff
git push origin develop
```

## Bonnes Pratiques pour les Commits

1. **Faites des commits fréquents et de petite taille**
   - Chaque commit doit représenter une seule modification logique
   - Évitez les commits avec des messages comme "WIP" ou "Fix"

2. **Utilisez des messages de commit informatifs**
   - Structure recommandée:
     ```
     Type: Court résumé (50 caractères max)

     Description détaillée si nécessaire. Expliquez le pourquoi plutôt que
     le comment. Limitez chaque ligne à 72 caractères.

     Référence à l'issue: #123
     ```
   - Types de commit:
     - `feat`: Nouvelle fonctionnalité
     - `fix`: Correction de bug
     - `docs`: Modification de la documentation
     - `style`: Formatage, point-virgule oubliés, etc. (pas de changement de code)
     - `refactor`: Refactorisation du code
     - `test`: Ajout de tests
     - `chore`: Mise à jour des outils, dépendances, etc.

3. **Liez les commits aux issues**
   - Référencez les issues dans les messages de commit: `#123`
   - Utilisez des mots-clés pour fermer automatiquement les issues: `Fixes #123`, `Closes #123`

## Utilisation des Pull Requests (PR)

1. **Créez des PR pour toutes les modifications significatives**
   - Donnez un titre clair et une description détaillée
   - Référencez les issues liées
   - Utilisez le template de PR fourni

2. **Demandez des revues de code**
   - Assignez au moins un relecteur
   - Répondez aux commentaires et apportez les modifications nécessaires

3. **Attendez l'approbation avant de merger**
   - Les PR doivent être approuvées par au moins un relecteur
   - Tous les tests doivent passer

4. **Utilisez "Squash and Merge" pour fusionner**
   - Consolidez les commits de travail en un seul commit propre
   - Le message du commit final devrait résumer toutes les modifications

## Gestion des Tags et Versions

- Utilisez le versionnement sémantique (SemVer): `MAJOR.MINOR.PATCH`
  - `MAJOR`: Changements incompatibles avec les versions précédentes
  - `MINOR`: Nouvelles fonctionnalités rétrocompatibles
  - `PATCH`: Corrections de bugs rétrocompatibles

- Créez des tags pour chaque version
  ```bash
  git tag -a v1.0.0 -m "Version 1.0.0"
  git push origin v1.0.0
  ```

## Outils Recommandés

- **GitHub Desktop** - Interface graphique pour Git
- **GitKraken** - Autre interface graphique puissante
- **Visual Studio Code** - Éditeur avec excellente intégration Git
- **GitHub CLI** - Interface en ligne de commande pour GitHub
