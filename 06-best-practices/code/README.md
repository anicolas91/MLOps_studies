# Python tests
## Getting started
We obtain the Pipfile and other files from the module 04, the streaming portion.

We use the present Pipfile and Pipfile.lock to instantiate a new python env via:
```bash
pipenv install
```

and we add pytest as a dev library via
```bash
pipenv install --dev pytest
```

You should end up seeing on VS code, under the `>Python: select interpreter` the `code-xxxxxx` venv with python 3.9.6.

If the venv looks odd, has issues locking, or is using the wrong python version, then you need to remove any preexisting venvs and start again.

To remove simply run
```bash
pipenv --rm
```

To run the pipenv simply do
```bash
pipenv shell
```

Also, if you already had the pipfile with the dev bit, then youll have to redo the install via
```bash
pipenv install --dev
```

Make sure then that you got python and pytest via
```bash
pipenv shell
which python
which pytest
```

## starting up tests on VS code
you need to 
- create a `tests` directory in your project
- install the `python` extension
- on the `tests` tab on the left, select `configure python tests` --> `pytest` --> `tests` during directory selection

## Creating a test
You basically create two files inside the tests folder:
- `__init__.py` to indicate that his is a library
- `model_test.py` where you will write your tests

Have a look inside the python script with the model tests. In general, if you have a workable test, it will be detected by VS code under the tests tab.

## Running a test
Either you run:
```bash
pipenv run pytest tests/
```

Or you use the UI in VS code on the tests tab.

Unit tests = they evaluate only small sections/units of the code

Integration tests = they cover the entire thing, you run it continously to make sure everything still works.