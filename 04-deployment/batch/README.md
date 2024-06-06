## Batch deployment

The steps are as follows:

1. Turn the notebook for training a model into a notebook for applying the model
   - you basically read in the pretrained model, and make sure you're just applying to whatever it is you're loading
   - the output is a pandas df with basic metadata, and the pred/actual durations
   - the notebook is all fcns so that the main bit is 1 function that takes in basic info like filepaths and run ids
  
2. Turn the notebook into a script
    To convert a jupyter notebook into a script run:
    ```bash
    jupyter nbconvert --to script score.ipynb
    ```
    That will create a `score.py` file in the same folder. You just need to format it a little so that it runs as main.

3. Clean it and parametrize
   Basically just:
   - move everything into a run function that runs under main
   - use the sys library to set arguments as the parametrized input