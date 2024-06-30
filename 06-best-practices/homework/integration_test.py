import os
from utils import dt
import pandas as pd
import batch

data = [
(None, None, dt(1, 1), dt(1, 10)), # 9 mins difference
(1, 1, dt(1, 2), dt(1, 10)), # 8 mins difference
(1, None, dt(1, 2, 0), dt(1, 2, 59)), #59 seconds difference
(3, 4, dt(1, 2, 0), dt(2, 2, 1)), # 1 second difference
]

columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df = pd.DataFrame(data, columns=columns)

#save the data
year = 2023
month = 1
input_file = batch.get_input_path(year, month)
batch.save_data(filename=input_file,df=df)

print(input_file)

# call the batch script, set before env variables
# env variables are INPUT_FILE_PATTERN and OUTPUT_FILE_PATTERN
os.system('python batch.py 2023 1')

# read in saved answer
output_file = batch.get_output_path(year, month)
df_output = batch.read_data(output_file)

# calculate total duration
total_duration_actual= df_output['predicted_duration'].sum()
print(f"predicted duration total: {total_duration_actual:.2f}")

#check that value is correct and return go/nogo
total_duration_expected  = 36.28
assert abs(total_duration_expected-total_duration_actual) < 1
print('all good.') #wont print if assertion error btw