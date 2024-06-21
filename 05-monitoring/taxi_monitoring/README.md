# Monitoring using Evidently AI

## Getting started
### Setting up the env variable
- We first set up the env variable through conda as:
```bash
conda create -n py11 python=3.11
```
And then we add the required libraries via:
```bash
conda activate py11
pip install -r requirements.txt
```

### Setting up the Docker compose yml file
- We add on the main folder the `docker-compose.yml` file.
- We add a `config` folder with the grafana yml files called on the docker compose file.
- we add a `dashboards` folder for the fun of it since docker will use it later.
- We build up the docker image via:
```bash
docker compose up --build
```

NOTE: `--build` is only called when this is the first time creating these containers before.

### Accessing graphana
- After composing the docker container, go to [http://localhost:3000](http://localhost:3000)
- Input the following credentials:
  - user: admin
  - password: admin
- Graphana will ask you to change the password. Do that. In our case we used `oneprettybird` with the fancy formatting we usually use.

### Accessing Adminer
- After composing the docker container, go to [http://localhost:8080](http://localhost:8080)

## Creating artifacts for building a graphene dashboard
We will create the models, although you can use the ones already done in previous sections really.
- We read in training and validation data
- We clean the training data from outliers, and use the data to train a model
- We select a good model that has good quality metrics on both training and validation data.
- We save that model as a bin file.
- We save the validation data as reference data for later drift evaluations.

## Evidently
### creating results report
You basically import the following libraries usually:
```python
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric
```

And then create a report object like so:
```python
report = Report(
    metrics = [
        ColumnDriftMetric(column_name='prediction'), # prediction column in validation data will be assess for drift
        DatasetDriftMetric(),
        DatasetMissingValuesMetric()
    ]
)

column_mapping = ColumnMapping(
    target=None,
    prediction='prediction', # name on valiadation data
    numerical_features=num_features,
    categorical_features=cat_features
)

report.run(reference_data=train_data,current_data=val_data,column_mapping=column_mapping)

```

You can convert the report as a dictionary via:
```python
result = report.as_dict()
```

### Creating a dashboard
You start it via creating a workspace and an associated project
```python
from evidently.ui.workspace import Workspace 

ws = Workspace['workspace']
project = ws.create_project('NYC taxi data quality project')
```

Then you create a report and add it to the workspace. It is good practice to regularly create these reports and add it to the project for tracking.

In this case we are making a report for jan 28

```python
regular_report = Report(
    metrics = [
        DataQualityPreset()
    ],
    timestamp=datetime.datetime(2022,1,28) # specifying timestamp as jan 28
)
```

When we run the report we can use the btw function to get the associated data for jan 28
```python
regular_report.run(reference_data=None,
                  current_data=val_data.loc[val_data.lpep_pickup_datetime.between('2022-01-28', '2022-01-29', inclusive="left")],
                  column_mapping=column_mapping)
```

When you are happy with the report you get, you can add it to the workspace:

```python
ws.add_report(project.id, regular_report)
```

Then we move to the terminal to see what the project looks like. Run
```bash
evidently ui
```

Make sure you are under the folder where youre jupyter file is located.

You can go to http://0.0.0.0:8000 to see the evidently ui. You should see 3 tabs inside the project just generated:
- dashboard --> should be empty right now
- reports --> if you click on view you can see the report printed on jupyter
- test suites 

#### Adding a dashboard
First you configure the dashboard by adding a panel first (panel counter) :
```python
project.dashboard.add_panel(
    DashboardPanelCounter(
        filter=ReportFilter(metadata_values={}, tag_values=[]),
        agg=CounterAgg.NONE,
        title="NYC taxi data dashboard"
    )
)
```

On the project we added 2 more panels, look at the jupyter notebook for more info. It was essentially to add plots like for inference count or no of missing values:
```python
project.dashboard.add_panel(
    DashboardPanelPlot(
        filter=ReportFilter(metadata_values={}, tag_values=[]),
        title="Inference Count",
        values=[
            PanelValue(
                metric_id="DatasetSummaryMetric",
                field_path="current.number_of_rows",
                legend="count"
            ),
        ],
        plot_type=PlotType.BAR, #other options are line, scatter
        size=WidgetSize.HALF, # size of the panel, half of screen
    ),
)
```

After we add all the panels we like, we save the project to update everything
```python
project.save()
```

We can now go back to the UI to see how it looks now. Recommend to just run once because otherwise the same dashboard will be created several times.

When you have only 1 report, the dashboard will only plot a single point.


#### Adding another report for another datapoint
We just create a secondary report and change the date to jan 29.

We add the report to the project, and now we should see a second point plotted on the dashboard alongside a report for jan 29 on the list inside the ui


## Exiting docker
simply run

```bash
docker compose down
```

to close down the docker container and continue working with other stuff.

## graphana
- We start with a script to calculate some metrics that we care about.
- Then we create a tool to run that metric script every now and then and load stuff into the database.
- We also will have libraries for logging and stuff

### calculating metrics

#### Dummy metrics
We created the `dummy_metrics_calculation.py` script, which:
- creates a db and a table
- creates 3 random variables for funsies
- writes a 100 of those alongside a timestamp every 10 secs

in all of this the script is contacting the sql table using the credentials set up for postgres in the `docker-compose.yml` file:

```python
with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn: # we connect to host
```

To run this file we need our docker container, so set it up via
```bash
docker-compose up --build
```

and then test the script via

```bash
python dummy_metrics_calculation.py
```
Every 10 secs it will tell you that data will be sent.

Once it completes, go to http://localhost:8080/ and on the login fill the following:
- system: postgresQL
- server: db
- username: postgres
- password: example
- database: test

You should see a table inside with dummy metrics.

Then go to the dashboard in graphana http://localhost:3000

and now you can create a new dashboard in grafana using the postgreSQL db as input

#### NOTE:
Make sure your dashboard yml file contains the following:
```yaml
datasources:
  - name: PostgreSQL
    type: postgres
    access: proxy
    url: db:5432
    database: test
    user: postgres
    secureJsonData:
      password: 'example'
    jsonData:
      sslmode: 'disable'
      database: test
```

The original has a typo on url and has the database missing on jsondata

#### Evidently metrics

We created the `evidently_metrics_calculation.py` script, which:
- creates a db and a table
- creates an evidently report and extracts 3 metrics from it
- grabs the feb 2022 data and evaluates the metric day by day for a total of 28 points

It basically just updates the `calculate_metrics_postgresql` function by establishing the following metrics as output:

```python
#1st metric: prediction drift score
prediction_drift = result['metrics'][0]['result']['drift_score']
# 2nd metric: no of predicted columns
num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
# 3rd metric: no of missing values
share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']
```

where `result` is the dictionarized version of the report. For more details refer to the jupyter notebook.

#### Prefect
When using prefect as a pileline you essentially add flags such that:
- fcns --> tasks
- main --> flow



