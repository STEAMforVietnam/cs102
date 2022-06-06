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
