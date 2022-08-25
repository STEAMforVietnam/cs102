# STEAM for Vietnam - CS 102

Code and artifacts for CS 102 course.

## Setup Development Env

You only need to do these steps once:

1. Clone repo
2. `cd cs102/`
3. Create python virtualenv with python3: `python3 -m venv venv`
4. Install dependencies: `pip install -r requirements-dev.txt && pip install -r requirements.txt`
5. Activate githook: `pre-commit install --hook-type pre-commit`

You will do these steps regularly: 

6. Activate virtualenv: `source venv/bin/activate`
7. Run game: `python src/main.py`

Now you can move on to [Deverloper's Guide](DEVGUIDE.md) to learn the high level architecture and dev tips.
