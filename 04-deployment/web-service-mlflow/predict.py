import pickle
from flask import Flask, request, jsonify
import mlflow
from mlflow.tracking import MlflowClient

RUN_ID = 'dadfadfas' #update this later
MLFLOW_TRACKING_URI = '127.0.0.1:5000'

# open the model registry and load the model
logged_model = f'runs/{RUN_ID}/model'
model = mlflow.pyfunc.load_model(logged_model)

# open the artifacts to download the dictionary vectorizer
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
path = client.download_artifacts(run_id=RUN_ID,path='dict_vectorizer.bin')
with open(path,'rb') as f_out:
    dv = pickle.load(f_out)

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