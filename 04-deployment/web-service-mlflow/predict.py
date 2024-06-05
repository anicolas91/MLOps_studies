import pickle
from flask import Flask, request, jsonify
import mlflow
from mlflow.tracking import MlflowClient

'''
NOTE: 
We are loading saved models and preprocessores from the
02-experiment-tracking module, where we used MLFlows UI
and we manually asked it to save the model and the preprocessor
via artifact logging.

To enter the db, simply change the working folder to:
MLOps_studies/02-experiment-tracking/

and then run the following to startup mlflow:
mlflow ui --backend-store-uri sqlite:///mlflow.db

once that is done check the UI in:
http://127.0.0.1:5000

in there you can find that the only run that has both the model
and the preprocessor is glamorous-turtle-248
also known as RUN_ID 0b983bbfdc7148a3951d7bce9c997594

NOTE: DONT FORGET TO ADD MLFLOW TO YOUR VENV
go to 04-deployment/web-service-mlflow/ and run:
pipenv install mlflow

'''

RUN_ID = '0b983bbfdc7148a3951d7bce9c997594' 
MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# open the model registry and load the model
logged_model = f'runs:/{RUN_ID}/models_mlflow'
model = mlflow.pyfunc.load_model(logged_model)

# open the artifacts to download the dictionary vectorizer
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
path = client.download_artifacts(run_id=RUN_ID,path='preprocessor.b')
with open(path,'rb') as f_out:
    dv = pickle.load(f_out)

print(f'downloading dict vectorizer to {path}')

# create function to prepare features
# we concatenate the categoricals and leave the numerical as is
def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

# create function to predict using the model
def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
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
        'duration': pred
    }
    return jsonify(result)

# set up main to run app on local port
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=9696)