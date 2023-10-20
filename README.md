### Prerequisites

- Docker CLI
- Python 3.8

### Install dependencies

A requirements file declare all dependencies (Mangum, FastAPI, Uvicorn, ...). Use the following command to install the required dependencies (For Python 3.8.5)

```
pip install -r ./requirements.txt
```

TIP : Before installing required dependencies, do not forget to create a virtual environment using your favorite tool (Conda, ...).

### Run locally

1- export environment variables ( HAZUS_DAMAGE_CURVE_CSV)


2- You can either use the following command :

```
python -m app.main
```

Or deploy on uvicorn :

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

### Test locally

You can test the application by using the following command : 

```
curl http://localhost:5000/docs/
```

### Build the container for AWS Lambda

Now we can build the container for AWS Lambda which will use the Mangum handler. We use another Dockerfile which will use a base image provided by AWS :

```
aws ecr get-login-password --region ca-central-1 | docker login --username AWS --password-stdin 101424409419.dkr.ecr.ca-central-1.amazonaws.com

docker build -t mediator-api . -f Dockerfile.aws.lambda

docker tag mediator-api:latest 101424409419.dkr.ecr.ca-central-1.amazonaws.com/mediator-api:latest

docker push 101424409419.dkr.ecr.ca-central-1.amazonaws.com/mediator-api:latest
```

### Deploy the application on AWS

[Step by step guide to deploy the application on AWS using console](./documentation/deployment/awsconsole/aws_console.md)
