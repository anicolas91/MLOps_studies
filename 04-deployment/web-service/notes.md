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

### NOTES
#### Using gunicorn

Flask is only for development, for production/deployment use gunicorn
```bash
 pipenv install gunicorn
```

and bind the address with:
```bash
gunicorn --bind=0.0.0.0:9696 predict:app
```
you basically are saying the address on what this runs `0.0.0.0:9696`, and to go to the `predict` module and search for the app named `app`

#### Installing packages that are only used during development
When we run tests such as `tests.py` we use the `requests` library, which is not necessary for the `predict.py` main python script.

We can install this library and specify that this library is only available during development via:

```bash
pipenv install --dev requests
```

Make sure to be on your pipenv `web-services` already.

## 4. we package everything into docker
- We create a `Dockerfile` and establish the python image to download, usually ask for the slim version:
  ```Docker
  FROM python:3.9.6-slim
  ```
- We update pip
  ```Docker
  RUN pip install -U pip
  ```
- We install pipenv so we can run the pipfiles
  ```Docker
  RUN pip install pipenv
  ```
- We create a folder called `app` and move in there
  ```Docker
  WORKDIR /app
  ```
- We copy our pipfiles to the docker image (current directory)
  ```Docker
  COPY ["Pipfile","Pipfile.lock","./"]
  ```
- We install and open our pipenv to your 'main system' python inside the image
  ```Docker
  RUN pipenv install --system --deploy
  ```
- We copy into our docker image the prediction script and the bin model
  ```Docker
  COPY ["predict.py","lin_reg.bin","./"]
  ```
- We expose the port 9696 so that we tell that this port should be open
  ```Docker
  EXPOSE 9696
  ```
- We tell docker to run gunicorn
  ```Docker
  ENTRYPOINT ["gunicorn","--bind=0.0.0.0:9696","predict:app"]
  ```

### Building the docker image
To build the Docker image simply run:
```bash
docker build -t ride-duration-prediction-service:v1 .
```

Where -t is just the flag for a tag, and the `.` means that its the folder we are currently in.

### Running image in interactive mode
We can now run the Docker image in interactive mode by adding the `-it` tag, by specifying to `--rm` remove the image after we are done, and to map the port `-p` 9696 of the host machine on the port 9696 on the container.
```bash
docker run -it --rm -p 9696:9696 ride-duration-prediction-service:v1
```

Now when we run `test.py` it will use the Docker image instead of straight up gunicorn or our local Flask.

# NOTES:
- to shorten the long prompt on the terminal, simply run:
  ```bash
  PS1="> "
  ```