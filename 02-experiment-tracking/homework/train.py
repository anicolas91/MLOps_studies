import os
import pickle
import click

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import mlflow

#set up mlflow bits 
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("nyc-green-taxi-experiment")
mlflow.sklearn.autolog()

def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):
    with mlflow.start_run():
        mlflow.set_tag("model","sklearn")
        mlflow.set_tag("developer","andrea")
        mlflow.log_param("train-data-path", "../../data/green_tripdata_2023-01.csv")
        mlflow.log_param("valid-data-path", "../../data/green_tripdata_2023-02.csv")
        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)


if __name__ == '__main__':
    run_train()
