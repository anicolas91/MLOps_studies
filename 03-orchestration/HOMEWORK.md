# 03 - Orchestration HW
[http://localhost:6789/](http://localhost:6789/)

## Q1. Run mage

What is the version of mage we run?

### A: Version 0.9.70

## Q2. Creating a project

How many lines are in the created `metadata.yaml` file?

### A: freshly after creating the project, we have 55 lines of code.

## Q3. Creating a pipeline

We read the march 2023 yellow taxi trips data. How many records did we read?

### A: after loading from the NYC LTC website the yellow data info for march 2023, we ended up loading 3403766 rows of data.


## Q4. Data preparation

Create a transformer block to process the data given the code shared in class. What is the size of the result?

### A: After applying the cleanup seen in the previous module, the cleaned up dataset is 3316216 rows long.

## Q5. Train a model

Use the linear regression model to  train the data. So 
- fit a dict vectorizer
- train linear regresion with default params
- use pickup/dropoff as independent variables

What is the intercept of the model?

### A: for yellow taxis on march 2023, the lr fit intercept is 23.85

- for yellow taxis on jan 2023, the lr fit intercept is 21.84
- for gren taxis on jan 2023, the lr fit intercept is 21.49

## Q6. Register the model

Find the logged model, and find MLModel file. What's the size of the model? (model_size_bytes field):

### A: the pickle size of the fitted model is 5kb (4,542 bites)

#### NOTE: to get this running in mage, we needed to set the following:

- on the pipeline: mlflow.set_tracking_uri("http://mlflow:5000")
- on the browser: we visit 127.0.01:5000 (or localhost:5000, its the same)