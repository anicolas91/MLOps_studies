import pickle
import pandas as pd
import os
import sys

## Setting up functions
def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

def load_model(model_name='model.bin'):
    with open(model_name, 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return dv, model

def apply_model(year=2023,month=1,model_name='model.bin'):
    # set up filenames
    taxi_type = 'yellow'
    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'output/{taxi_type}/{year:04d}-{month:02d}.parquet'

    # read datasets
    df = read_data(input_file)
    dv, model = load_model(model_name)

    # applying model
    categorical = ['PULocationID', 'DOLocationID']
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    # set up ride id
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    # saving the results
    save_results(df,y_pred,output_file)

    return y_pred, output_file

def save_results(df: pd.DataFrame,y_pred,output_file):
    # creating the final results df
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['prediction'] = y_pred
    # saving as parquet file
    create_outfolder(output_file)
    df_result.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )
    return None

def create_outfolder(output_file):
    path = os.path.dirname(output_file)
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, path)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)


## Reading dataset and making a prediction
def run():
    year = int(sys.argv[1]) #2023
    month = int(sys.argv[2]) #1

    y_pred, _ = apply_model(
                    year=year,
                    month=month,
                    model_name='model.bin'
                )
    
    # print mean predicted duration
    print(f'For {month:02d}/{year:04d} the mean predicted duration is {y_pred.mean():.2f} minutes')

if __name__=='__main__':
    run()