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
