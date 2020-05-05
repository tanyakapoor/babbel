## Summary

`Programming with Python` Consider a scenario where a data scientist would like to track various currencies over time and invest his/her money to foreign currencies (from US Dollars). Write a Python application that fetches conversion rates for USD hourly, and appends them to a CSV file for further analysis. The structure of the dataset should ease the purpose of our data scientist and will be decided by you. You can use the API at https://exchangeratesapi.io/

## Installation

Install `docker` following [this link](https://docs.docker.com/docker-for-mac/install/)).

## Development

### Clone Git Submodule

`git clone git@github.com:tanyakapoor/babbel.git`

### Build docker image

`docker build --tag my-python-app .`

### Run

`docker run --name python-app -p 5000:5000 my-python-app`

### Stop and Remove image

`docker stop python-app & docker rm python-app`

### Login and check logs

`docker exec -it python-app bash`

`tail -f app.log`

`less data.csv`
