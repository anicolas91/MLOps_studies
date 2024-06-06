# Web service with MLFlow

We are loading saved models and preprocessores generated after running random-forest.ipynb, where we used MLFlows server and we manually asked it to save the model and the dv via artifact logging.

## Getting started with MLflow

Simply run the following to startup mlflow:

```bash 
mlflow server --backend-store-uri=sqlite:///mlflow.db --default-artifact-root=./artifacts_local/
```

once that is done check the UI in:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

in there you can find a run that has both the model and the preprocessor : `industrious-pug-605` ]palso known as `RUN_ID d4f23de4f6bb46d9a46893256a104d07`

### NOTE about virtual envs: 
DONT FORGET TO ADD MLFLOW TO YOUR VENV
go to `04-deployment/web-service-mlflow/` and run:
```bash
pipenv install mlflow
```

### NOTE About AWS S3
If the models/pipelines are saved on an s3 AWS bucket, you can just put the full s3 address under load_model to skip altogether the need for reading through the tracking server

it would be like:

```python
logged_model = s3://my_bucket/path/to/model
```

and there is no need to set the tracking uri

### NOTE about direct db loading
You can also just set up the RUN ID as an os env so you can work with kubernetes too.

in that case you would ask for the run id as:
```python
RUN_ID = os.get('RUN_ID')
```

in which the  run id is on bash set up as:
```bash
export RUN_ID='d4f23de4f6bb46d9a46893256a104d07'
```

So this can work via docker and whatnot