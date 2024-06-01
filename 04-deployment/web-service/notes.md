# Deploying a model as a web service

## 1. we create a virtual environment with pipenv

got to the `04-deployment/web-services/` folder and create a python environment with only scikit-learn and flask, you can also make sure that we're using the correct python version:
```bash
pipenv install scikit-learn==1.5.0 flask --python=3.9
```

this python environemnt will be isolated from the base libraries, and only contain the libraries needed for those two basic requirements.

You will see on your folder both a `Pipfile` and a `Pipfile.lock` files.

To activate this pyenv simply run:
```bash
pipenv shell
```

to exit this environment simply write `exit` or hit `ctrl+D`

## 2. we create a script for predicting
This file will contain the code for loading the model, scoring the request and all that. This is where the web service will be.

To do this we:
- create a `predict.py` file where we load the pickle file and we set the prediction function where the input is unprocessed features that gets properly preprocessed and transformed using the loaded dictionary vectorizer and adhoc functions.
- test using a fake input bit.

## 3. we put the script into a flask app
We basically wrap the script fcns into a flask wrapper bit that reads in json data, sends it to the python function, and reports out the result back to the system as a json object.

Basically start/create a Flask app, and don't forget to set your prediction fcn as endpoint:
```python
@app.route('/predict',methods=['POST'])
```

Note that the url to request will be, given say port `9696`:

```python
http://localhost:9696/predict
```

## 4. we package everything into docker


# NOTES:
- to shorten the long prompt on the terminal, simply run:
  ```bash
  PS1="> "
  ```