# steamvalley
Python game for CS 102

Game assets lấy từ: https://drive.google.com/drive/folders/10rFPJOfM5l65yLDjWa3o1H71gn5HcTY5

Internal CS 102 materials: https://coda.io/d/CS102-Masterplan_d9KVVJ8s4Bb/

## Structure

* Dung 1 repo cho nhieu games trong qua trinh thu nghiem, cac ban bat dau viet thu game thi co the lam trong `experimental/` roi thoai mai push code len `master` branch.
* Version chinh thuc nam rieng trong `src/`. Doi voi folder nay, ko push code len `master` branch ma phai thong qua PR va code review process.

## Setup Development Env

1. Clone repo
2. `cd steamvalley/`
3. Create python virtualenv with python3: `python3 -m venv venv`
4. Activate virtualenv: `source venv/bin/activate`
5. Install depedencies: `pip install -r requirements.txt`
5. Run game: `python src/main.py`

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
