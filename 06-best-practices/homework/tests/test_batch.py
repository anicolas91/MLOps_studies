from utils import dt
import pandas as pd
import batch

def test_prepare_data():
    data = [
    (None, None, dt(1, 1), dt(1, 10)), # 9 mins difference
    (1, 1, dt(1, 2), dt(1, 10)), # 8 mins difference
    (1, None, dt(1, 2, 0), dt(1, 2, 59)), #59 seconds difference
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)), # 1 second difference
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    categorical = ['PULocationID', 'DOLocationID']

    actual_df_dict = batch.prepare_data(df,categorical=categorical).to_dict()
    
    expected_df_dict = {
        'PULocationID': {0: '-1', 1: '1'}, 
        'DOLocationID': {0: '-1', 1: '1'}, 
        'tpep_pickup_datetime': {0: pd.Timestamp('2023-01-01 01:01:00'), 1: pd.Timestamp('2023-01-01 01:02:00')}, 
        'tpep_dropoff_datetime': {0: pd.Timestamp('2023-01-01 01:10:00'), 1: pd.Timestamp('2023-01-01 01:10:00')}, 
        'duration': {0: 9.0, 1: 8.0}
        }
    
    assert expected_df_dict == actual_df_dict