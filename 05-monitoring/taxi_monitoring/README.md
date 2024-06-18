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