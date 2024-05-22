# HOMEWORK - MLflow environment tracking

## Q1. install MLflow
What is the version of MLflow that you have?

A: mlflow, version 2.13.0


## Q2. Download and preprocess the data
How many files were saved to `output_folder`?

## Q3. Train model with autolog
what is the value of the `min_samples_split` parameter?

## Q4. Launch the tracking server locally
In addition to `backend-store-uri`, what else do you need to pass to properly configure the server?

## Q5. Tune model hyperparameters
What's the best validation RMSE that you got?

## Q6. Promote the best model to the model registry
What is the test RMSE of the best model?

# NOTES:
- To run GUI for mlflow: mlflow ui --backend-store-uri sqlite:///mlflow.db
  - backend will store all artifacts in sqlite