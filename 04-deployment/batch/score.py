#!/usr/bin/env python
# coding: utf-8

# # Random forest fitting
# This script is inspired on the 02-experiment-tracking HW, where you fit a bunch of random-forest models to the taxi data, and log onto MLflow both the fitted model as well as the dictionary vectorizer.
# 
# ## Starting up MLflow
# To start up mlflow, run on bash in this folder the following:
# ```bash
# mlflow server --backend-store-uri=sqlite:///mlflow.db --default-artifact-root=./artifacts_local/
# ```
# 
# Note that the default artifact root can be redone with an AWS bucket (s3) and that the backend store uri can just be a setup postgres

import pandas as pd
import mlflow
import os
import sys
import uuid # unique universal id


## Setting up functions

def create_outfolder(output_file):
    path = os.path.dirname(output_file)
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, path)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

def read_dataframe(filename: str):
    df = pd.read_parquet(filename)

    df['duration'] = df['lpep_dropoff_datetime'] - df['lpep_pickup_datetime']
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)
    df = df[(df.duration >= 1) & (df.duration <= 60)]

    df['ride_id'] = [str(uuid.uuid4()) for i in range(len(df))]

    return df

def prepare_dictionaries(df: pd.DataFrame):
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)

    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']
    categorical = ['PU_DO']
    numerical = ['trip_distance']
    dicts = df[categorical + numerical].to_dict(orient='records')
    return dicts

def load_model(run_id):
    logged_model = f'../web-service-mlflow/artifacts_local/1/{run_id}/artifacts/model'
    model = mlflow.pyfunc.load_model(logged_model)
    return model

def apply_model(input_file, run_id, output_file):
    print(f'reading the data from {input_file}...')
    df = read_dataframe(input_file)
    dicts = prepare_dictionaries(df)

    print(f'loading the model with RUN_ID= {run_id}...')
    model = load_model(run_id)
    y_pred = model.predict(dicts)

    print(f'saving the data to {output_file}...')
    df_result = pd.DataFrame()

    df_result['ride_id'] = df['ride_id']
    df_result['lpep_pickup_datetime'] = df['lpep_pickup_datetime']
    df_result['PULocationID'] = df['PULocationID']
    df_result['DOLocationID'] = df['DOLocationID']
    df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred
    df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']
    df_result['model_version'] = run_id

    # create output foldder if not exists
    create_outfolder(output_file)
    
    #save results
    df_result.to_parquet(output_file,index=False)

    print('saved.')

## Reading in the data and prepping dicts
# This time we are not training nor validating, we are just applying the model to predict things

def run():
    
    taxi_type = sys.argv[1] #'green'
    year = int(sys.argv[2]) #2023
    month = int(sys.argv[3]) #1
    run_id = sys.argv[4] #d4f23de4f6bb46d9a46893256a104d07

    input_file = f'../../data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'output/{taxi_type}/{year:04d}-{month:02d}.parquet'
    
    apply_model(
        input_file=input_file, 
        run_id = run_id, 
        output_file=output_file
    )


if __name__=='__main__':
    run()