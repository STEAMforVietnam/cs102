OOP Advance
===========

# How to Run
```sh
# source venv/bin/activate
# Go to current lesson directory
cd oop_advance
# Start from lesson root dir, to reuse `assets` folder
python cot_moc_1/main.py
```

# Lesson Plan
## Checkpoint 1: Python module & Multi-files project

Refactor our long python code into many files & import from each `module` (1 .py file -> 1 module):
- `common.py`: store all Constants, Styling (Colors & Fonts), Sprites (pre-loaded)
- `entities.py`: store models / definitions of all Game Entities
- `utils.py`: store helper functions (scale image, check overlapping, ...)
- `main.py`: main loop & game logic


## Checkpoint 2: Basic Inheritance
- Under `entities.py`, create new `BaseEntity` class and all game objects inherit from it
- Association concept by defining `touch` method under `BaseEntity`
- How to trigger parent class Constructors

## Checkpoint 3: Python Package
Refactor `entities.py` into `entities` folder (package)
- What's `__init__.py` file
- How to import from a package

## Checkpoint 4
- Introduction of `World` object

## Checkpoint 5
- Introduction of `WorldManager` concept
- Reload game on Enter
