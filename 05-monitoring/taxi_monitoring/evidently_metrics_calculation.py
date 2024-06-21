import datetime
import time
import random
import logging # to show something in terminal
import uuid #unique ids
import pytz #timezones
import pandas as pd
import io #writing into file system
import psycopg # to access the database
import joblib # to load the model

# this time we add evidently
from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric

# we specify the loggin option and then create the database together with the table
# we specify how to log the data, with time, level and message
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

# we create a couple of global variables, like sending data timeout and random generator
SEND_TIMEOUT = 10
rand = random.Random()

# we create fcn to prepare the database
# we check if the test db exists, if not we create it, if we do, we create a table

# this is the SQL statement to create a new table, this time with the evidently metrics
create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics(
	timestamp timestamp,
	prediction_drift float,
	num_drifted_columns integer,
	share_missing_values float
)
"""

# read the reference data and model
reference_data = pd.read_parquet('data/reference.parquet')
with open('models/lin_reg.bin', 'rb') as f_in:
	model = joblib.load(f_in)

# we read the whole production data
# usually here it is a pipeline manager, but for now we just read in the raw data as a whole
raw_data = pd.read_parquet('data/green_tripdata_2022-02.parquet')

# we set up the beginning time, in this case is feb 1st 2022
begin = datetime.datetime(2022, 2, 1, 0, 0)

# bits needed to create the evidently report necessary for evidently metrics
num_features = ['passenger_count', 'trip_distance', 'fare_amount', 'total_amount']
cat_features = ['PULocationID', 'DOLocationID']

column_mapping = ColumnMapping(
    target=None,
    prediction='prediction', # name on valiadation data
    numerical_features=num_features,
    categorical_features=cat_features
)

report = Report(
    metrics = [
        ColumnDriftMetric(column_name='prediction'), # prediction column in validation data will be assess for drift
        DatasetDriftMetric(),
        DatasetMissingValuesMetric()
    ]
)

# preparation fcn
def prep_db():
	with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn: # we connect to host
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'") # this is an sql query
		if len(res.fetchall()) == 0: #if there is no database...
			conn.execute("create database test;") # we create the test database
		with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example") as conn: # we connect to the db 
			conn.execute(create_table_statement) # we create the table

# we calculate ACTUAL metrics fcn
# you need to have a report first from which to obtain the metrics
def calculate_metrics_postgresql(curr, i): # we insert values in the curr position oh the cursor
	# set up the current data, where i is the number of day in a month... were calculating the values month by month
	current_data = raw_data[(raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(i))) &
		(raw_data.lpep_pickup_datetime < (begin + datetime.timedelta(i + 1)))]
	#current_data.fillna(0, inplace=True)
	current_data['prediction'] = model.predict(current_data[num_features + cat_features].fillna(0))
	# create the report
	report.run(reference_data=reference_data,current_data=current_data,column_mapping=column_mapping)
	# convert to dictionary
	result = report.as_dict()
	# extract the metrics as needed
	
	#1st metric: prediction drift score
	prediction_drift = result['metrics'][0]['result']['drift_score']
	# 2nd metric: no of predicted columns
	num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
	# 3rd metric: no of missing values
	share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']

	# insert data into table day by day
	curr.execute(
		"insert into dummy_metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_values) values (%s, %s, %s, %s)",
		(begin + datetime.timedelta(i), prediction_drift, num_drifted_columns, share_missing_values)
	)

# fcn to iterate a number of times in a cycle
def main():
	prep_db() # just preps db and table
	last_send = datetime.datetime.now() - datetime.timedelta(seconds=10) # time of last sent
	with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example", autocommit=True) as conn: # connected to db w credentials
		for i in range(0, 27): #iterated 28 days of february
			with conn.cursor() as curr: # inserted on cursor ACTUAL metrics and timestamp
				calculate_metrics_postgresql(curr, i)

			new_send = datetime.datetime.now()
			seconds_elapsed = (new_send - last_send).total_seconds() # for visuals we have a time delay calc
			if seconds_elapsed < SEND_TIMEOUT: # if its less than the 10 secs we just wait
				time.sleep(SEND_TIMEOUT - seconds_elapsed)
			while last_send < new_send: # if more than 10 secs passed then sure send the data
				last_send = last_send + datetime.timedelta(seconds=10)
			logging.info("data sent")


if __name__ == '__main__':
	main()