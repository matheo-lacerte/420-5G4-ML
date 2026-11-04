# Repository Guide

This repository contains three independent workshop sections: Pokemon ML notebooks in `apprentissage/`, image-classification notebooks in `analyse_image/`, and a C++ library-management CLI in `agent/`.

## C++ CLI (`agent/`)

- Build from the repository root: `cmake -S agent -B agent/build && cmake --build agent/build`.
- Run with the bundled fixtures: `./agent/build/bibliotheque -d agent/data`.
- The CLI writes `books.txt` and `users.txt` when saving or exiting. Use a copied data directory for interactive checks so tracked fixtures are not changed.
- `agent/CMakeLists.txt` includes every `agent/*.cpp`, requires C++17, and enables `-Wall -Wextra -Wpedantic`.

## Notebooks

- Execute notebooks from their own directory: their data and model paths are relative to that directory.
- Run the Pokemon notebooks in order: `partie1_2.ipynb` generates `data/dataset.csv`; `partie3_entrainement.ipynb` writes `modele/modele_pokemon.mod`; `partie3_predictions.ipynb` loads that model.
- The notebook metadata uses the `.venv` Python 3.12.3 kernel. No Python dependency manifest is committed.
- `analyse_image/classification.ipynb` expects untracked `data/fashion-mnist_train.csv` and `data/fashion-mnist_test.csv`; the committed IDX files do not satisfy those paths. `test_model.ipynb` loads the committed model files and `data/image.png`.

## Verification

- No CI, formatter, linter, or automated test configuration is committed. For C++ changes, build the target above; notebook changes require running the affected notebook with its required data available.
