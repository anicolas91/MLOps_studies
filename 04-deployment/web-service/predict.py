import pickle
from flask import Flask, request, jsonify

# open the model from a pickle file
with open('lin_reg.bin','rb') as f_in:
    (dv,model) = pickle.load(f_in)

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
    return preds[0] 
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