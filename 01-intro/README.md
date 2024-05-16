## Local envprep
basically, you need the latest anaconda and Docker desktop.

### for anaconda:

````
brew install anaconda --cask
````
If it was already installed it will only update it.

### for docker:

````
brew install docker --cask
````

if you already had it installed it will just not do it.

Make sure docker works using:
````
docker run hello-world
````

## Data aquisition
Data comes from the NYC taxi trip record data [here](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

We downloaded the yellow and green taxi info for jan and feb 2023.

The homework looks at the ***Yellow*** taxi data.