import datetime
import time
import random
import logging # to show something in terminal
import uuid #unique ids
import pytz #timezones
import pandas as pd
import io #writing into file system
import psycopg # to access the database

# we specify the loggin option and then create the database together with the table
# we specify how to log the data, with time, level and message
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

# we create a couple of global variables, like sending data timeout and random generator
SEND_TIMEOUT = 10
rand = random.Random()

# we create fcn to prepare the database
# we check if the test db exists, if not we create it, if we do, we create a table

# this is the SQL statement to create a new table
create_table_statement = """
drop table if exists dummy_metrics;
create table dummy_metrics(
	timestamp timestamp,
	value1 integer,
	value2 varchar,
	value3 float
)
"""

# preparation fcn
def prep_db():
	with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn: # we connect to host
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'") # this is an sql query
		if len(res.fetchall()) == 0: #if there is no database...
			conn.execute("create database test;") # we create the test database
		with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example") as conn: # we connect to the db 
			conn.execute(create_table_statement) # we create the table

# we calculate dummy metrics fcn
def calculate_dummy_metrics_postgresql(curr): # we insert values in the curr position oh the cursor
	value1 = rand.randint(0, 1000) # random integer from 0 to 1000
	value2 = str(uuid.uuid4()) # unique id string
	value3 = rand.random() # full random value

	curr.execute(
		"insert into dummy_metrics(timestamp, value1, value2, value3) values (%s, %s, %s, %s)",
		(datetime.datetime.now(pytz.timezone('Europe/London')), value1, value2, value3)
	)

# fcn to iterate a number of times in a cycle
def main():
	prep_db() # just preps db and table
	last_send = datetime.datetime.now() - datetime.timedelta(seconds=10) # time of last sent
	with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example", autocommit=True) as conn: # connected to db w credentials
		for i in range(0, 100): #iterated 100 times
			with conn.cursor() as curr: # inserted on cursor dummy metrics and timestamp
				calculate_dummy_metrics_postgresql(curr)

			new_send = datetime.datetime.now()
			seconds_elapsed = (new_send - last_send).total_seconds() # for visuals we have a time delay calc
			if seconds_elapsed < SEND_TIMEOUT: # if its less than the 10 secs we just wait
				time.sleep(SEND_TIMEOUT - seconds_elapsed)
			while last_send < new_send: # if more than 10 secs passed then sure send the data
				last_send = last_send + datetime.timedelta(seconds=10)
			logging.info("data sent")


if __name__ == '__main__':
	main()