import pickle
from flask import Flask, request, jsonify
import mlflow
from mlflow.tracking import MlflowClient

'''
We are loading saved models and preprocessores generated after 
running random-forest.ipynb, where we used MLFlows server
and we manually asked it to save the model and the dv
via artifact logging.

Simply run the following to startup mlflow:
mlflow server --backend-store-uri=sqlite:///mlflow.db 
--default-artifact-root=./artifacts_local/

once that is done check the UI in:
http://127.0.0.1:5000

in there you can find a run that has the pipeline : industrious-pug-605
also known as RUN_ID d4f23de4f6bb46d9a46893256a104d07

NOTE: DONT FORGET TO ADD MLFLOW TO YOUR VENV
go to 04-deployment/web-service-mlflow/ and run:
pipenv install mlflow

NOTE 2: if the models/pipelines are saved on an s3 AWS bucket, you can just 
put the full s3 address under load_model to skip altogether the need for 
reading through the tracking server

it would be like: only
logged_model = s3://my_bucket/path/to/model

and there is no need to set the tracking uri

NOTE 3: you can also just set up the RUN ID as an os env so you can work with 
kubernetes too

in that case you would ask for the run id as:
RUN_ID = os.get('RUN_ID')

in which the  run id is on bash set up as:
export RUN_ID='d4f23de4f6bb46d9a46893256a104d07'

So this can work via docker and whatnot
'''

RUN_ID = 'd4f23de4f6bb46d9a46893256a104d07' 
MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# open the model registry and load the model/dv
logged_model = f'runs:/{RUN_ID}/model'
model = mlflow.pyfunc.load_model(logged_model)

# create function to prepare features
# we concatenate the categoricals and leave the numerical as is
def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

# create function to predict using the model
def predict(features):
    #X = dv.transform(features)
    preds = model.predict(features)
    return float(preds[0])
# note that the system wont print on json a list, it has to be the actual value

# start a flask application
app = Flask('duration-prediction')

# convert our prediction fcn into an endpoint
@app.route('/predict',methods=['POST'])
# create a fcn to wrap everything
# to take requests and write out the predictions
def predict_endpoint():
    ride = request.get_json() # read in request
    # process the thing
    features = prepare_features(ride)
    pred = predict(features)
    # report it out
    result = {
        'duration': pred,
        'model_version': RUN_ID
    }
    return jsonify(result)

# set up main to run app on local port
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=9696)