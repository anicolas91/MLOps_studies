import model

# prepare a test
def test_prepare_features():
    # example ride where we know the answer
    ride ={
        "PULocationID":130,
        "DOLocationID":205,
        "trip_distance":3.66
    }
    # check out the function we're testing
    model_maker = model.ModelMaker(None)
    actual_features = model_maker.prepare_features(ride)
    
    # set up the expected outcome
    expected_features = {
        "PU_DO": "130_205",
        "trip_distance":3.66
    }

    # compare and eval
    assert actual_features == expected_features

# evaluate model predictions
class ModelMock:
    def __init__(self,value):
        self.value = value
    def predict(self, X):
        n = len(X)
        return [self.value] * n
    
def test_predict():
    # import both mock model and the actual modelmaker
    mock_model = ModelMock(10.0)
    model_maker = model.ModelMaker(mock_model)
    #setup test features
    features = {
        "PU_DO": "130_205",
        "trip_distance":3.66
    }
    # evaluate output from mode
    actual_prediction = model_maker.predict(features)
    expected_prediction = 10.0 # only 1 input

    # compare and eval
    assert actual_prediction == expected_prediction