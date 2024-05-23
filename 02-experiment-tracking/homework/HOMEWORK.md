# HOMEWORK - MLflow environment tracking

## Q1. install MLflow
What is the version of MLflow that you have?

### Answer
After running `mlflow --version` we get that mlflow is version 2.13.0


## Q2. Download and preprocess the data
How many files were saved to `output_folder`?

### Answer
After running `python preprocess_data.py --raw_data_path ../../data/ --dest_path ./output`, we get 4 files:

1. dv.pkl
2. test.pkl
3. train.pkl
4. val.pkl

## Q3. Train model with autolog
what is the value of the `min_samples_split` parameter?

### Answer
After running both `mlflow ui --backend-store-uri sqlite:///mlflow.db` and `python train.py` we find on the experiment inside [http://127.0.0.1:5000/](http://127.0.0.1:5000/) that `min_samples_split==2`.

## Q4. Launch the tracking server locally
In addition to `backend-store-uri`, what else do you need to pass to properly configure the server?

### Answer
To launch a server locally you need `default-artifact-root` when backend store is not local file based (meaning you are using an sqlite database)

### NOTES:
We launched the tracking server locally by running:
`mlflow server --backend-store-uri sqlite:///backend.db --default-artifact-root ./artifacts_local`

## Q5. Tune model hyperparameters
What's the best validation RMSE that you got?

### Answer
After running `python hpo.py` we find on the experiment `random-forest-hyperopt` inside [http://127.0.0.1:5000/](http://127.0.0.1:5000/) that the best validation RMSE is `5.335`

## Q6. Promote the best model to the model registry
What is the test RMSE of the best model?

### Answer
After running `python register_moddel.py` we find on the experiment `random-forest-best-models` inside [http://127.0.0.1:5000/](http://127.0.0.1:5000/) that the best validation RMSE is `5.567`

# NOTES:
- To run GUI for mlflow: mlflow ui --backend-store-uri sqlite:///mlflow.db
  - backend will store all artifacts in sqlite