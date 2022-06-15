# steamvalley
Python game for CS 102

Game assets lấy từ: https://drive.google.com/drive/folders/10rFPJOfM5l65yLDjWa3o1H71gn5HcTY5

Internal CS 102 materials: https://coda.io/d/CS102-Masterplan_d9KVVJ8s4Bb/

## Structure

* Dung 1 repo cho nhieu games trong qua trinh thu nghiem, cac ban bat dau viet thu game thi co the lam trong `experimental/` roi thoai mai push code len `master` branch.
* Version chinh thuc nam rieng trong `src/`. Doi voi folder nay, ko push code len `master` branch ma phai thong qua PR va code review process.

## Setup Development Env

You only need to do these steps once:

1. Clone repo
2. `cd steamvalley/`
3. Register `githooks` dir: `git config core.hooksPath githooks`
4. Create python virtualenv with python3: `python3 -m venv venv`

You will do these steps regularly: 

5. Activate virtualenv: `source venv/bin/activate`
6. Install dependencies: `pip install -r requirements-dev.txt && pip install -r requirements.txt`
7. Run game: `python src/main.py`

## Python3 typing

We use `mypy` for static typing checking. Call it with the root of a subproject:

```shell
mypy src  # checking main project
mypy lessons/oop_advance/cot_moc_5/  # check the specific lesson checkpoint
```

**It will shows you all the typing errors. Please attempt to fix as much as possible
(we do NOT enforce zero error yet).**

## Code Linter

We use [black](https://black.readthedocs.io/en/stable/) and [flake8](https://flake8.pycqa.org/)
to keep the code easy to read and adhere to Python guidelines.

`black` can be run like this:

```shell
$ black src
reformatted src/common/util.py
reformatted src/game_entities/base_entity.py
reformatted src/game_entities/movable_entity.py
reformatted src/game_entities/animated_entity.py

All done! ✨ 🍰 ✨
4 files reformatted, 7 files left unchanged.
```

It will also run automatically whenever you do `git commit` as a pre-commit hook.
If either `black` or `flake8` fails to auto-format your code, you need to go fix the format errors before continue.

## Do's and Dont's

1. Instead of `print`, use standard `logging` library

Add these lines at the beginning of src code file:

```python
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

Use the `logger`:

```python
logger.debug(...)
logger.info(...)
logger.warning(...)
```


## Architecture

The outer loop in `main.py` calls `self.scene_manager.tick()` every game tick.

`self.scene_manager.tick()` query ALL un-processed events in the Event queue by this line:

```python
events = pygame.event.get()
```

These events are sent to game entities to handle in the `.update(events, world)` function. 


## Story Design Guide

### Game entity

Game entities are every subject / object in the game: player, each enemy, NPCs, etc.

### Scene data

Scene data are in `.csv` files, which tells the game where each game entity is.

### How to add a new NPC

For example, we want to add `npc_co_nga.png`
(this is for non-animated NPCs,
 for animated NPCs, similar but slightly different - will discuss later)

1. Add image to `assets/tiles/`
2. Go to `common/types.py`, add a new enum to `TileType`, enum name is uppercase of image name: `NPC_CO_NGA`, enum value is an integer different from existing other TileType values
3. Add NPC to `.csv`  at desired location.

### Tips

* Can modify player speed and other settings in `config.py`.
* Basic interactions that can be included in the game story and quests: picking up items, dropping off items, open locked door with keys, etc.
* For other custom interactions: discuss with team to get them implemented
* You can use breakpoints and debug mode in Pycharm to debug
