## Batch deployment

The steps are as follows:

1. Turn the notebook for training a model into a notebook for applying the model
   - you basically read in the pretrained model, and make sure you're just applying to whatever it is you're loading
   - the output is a pandas df with basic metadata, and the pred/actual durations
   - the notebook is all fcns so that the main bit is 1 function that takes in basic info like filepaths and run ids
2. Turn the notebook into a script
3. Clean it and parametrize