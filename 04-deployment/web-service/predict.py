import pickle

# open the model from a pickle file
with open('lin_reg.bin','rb') as f_in:
    (dv,model) = pickle.load(f_in)

# create function to prepare features
# we concatenate the categoricals and leave the numerical as is
def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocation_ID'], ride['DOLocation_ID'])
    features['trip_distance'] = ride['trip_distance']
    return features

# create function to predict using the model
def predict(features):
    X = dv.transform(features)
    preds = model.predict(X)
    return preds