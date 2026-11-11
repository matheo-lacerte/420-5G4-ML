# Bibliotheque personnelle

Le projet contient une application C++ en ligne de commande et une interface graphique Python qui utilise le meme moteur C++.

## Installation et lancement

Depuis la racine du depot :

```bash
cmake -S agent -B agent/build && cmake --build agent/build
python3 -m venv agent/.venv
agent/.venv/bin/pip install -r agent/requirements.txt
agent/.venv/bin/python agent/gui/app.py
```

L'interface charge par defaut les fichiers de `agent/data`. Pour choisir un autre repertoire :

```bash
agent/.venv/bin/python agent/gui/app.py --data-dir chemin/vers/data
```

## Interface graphique

Les fonctionnalites actuellement implementees sont :

- Consulter le catalogue et les statistiques de la bibliotheque.
- Rechercher un livre par titre ou auteur.
- Filtrer les livres disponibles.
- Ajouter un livre avec son titre, auteur et ISBN.
- Supprimer un livre disponible.
- Ajouter un lecteur avec son nom et son ID.
- Afficher les lecteurs et la liste de leurs emprunts.
- Emprunter un livre disponible a un lecteur existant.
- Retourner un livre emprunte.
- Creer des copies `books.txt.backup` et `users.txt.backup`.

L'ajout et la suppression de livres modifient immediatement `books.txt`. L'ajout d'un lecteur modifie `users.txt`. Un emprunt ou un retour modifie les deux fichiers. Utilisez un autre repertoire avec `--data-dir` pour tester sans modifier les donnees fournies.

## Ligne de commande

Pour lancer la version terminal avec les donnees fournies :

```bash
./agent/build/bibliotheque -d agent/data
```

## Repertoire de donnees

Le repertoire de donnees doit contenir `books.txt` et `users.txt`.
