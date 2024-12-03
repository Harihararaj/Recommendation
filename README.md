
# Recommender System with SageMaker Deployment

This repository contains a Flask-based Recommender System deployed on AWS SageMaker using a custom Docker container. The system uses Apache Spark's MLlib for recommendations and SageMaker for serving predictions via an endpoint.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Docker Image](#docker-image)
- [Deploying to SageMaker](#deploying-to-sagemaker)
- [Testing the Endpoint](#testing-the-endpoint)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have the following tools and resources:

1. **AWS Account**: Make sure you have an active AWS account.
2. **AWS CLI**: Install and configure the AWS CLI with appropriate credentials.
   ```bash
   aws configure
   ```
3. **Docker**: Install Docker on your system.
4. **Python**: Python 3.8+ with `boto3` installed.
   ```bash
   pip install boto3
   ```

---

## Project Structure

The repository is organized as follows:

```
.
├── app/
│   ├── serve.py                # Flask app to serve the recommendation model
│   ├── als_model/              # Serialized ALS model (Spark MLlib format)
│   ├── requirements.txt        # Python dependencies
├── Dockerfile                  # Dockerfile for building the container
└── README.md                   # This documentation
```

---

## Docker Image

### Building the Docker Image
To build the Docker image, run the following command:

```bash
docker build -t recommender .
```

### Testing Locally
Run the Docker container locally to ensure it works:

```bash
docker run -p 8080:8080 recommender
```

Visit `http://127.0.0.1:8080` in your browser or use a tool like Postman to send test requests.

---

## Deploying to SageMaker

### Step 1: Push the Docker Image to AWS ECR
1. Authenticate Docker to your ECR registry:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account_id>.dkr.ecr.us-east-1.amazonaws.com
   ```

2. Tag the Docker image:
   ```bash
   docker tag recommender:latest <account_id>.dkr.ecr.us-east-1.amazonaws.com/recommender:latest
   ```

3. Push the image:
   ```bash
   docker push <account_id>.dkr.ecr.us-east-1.amazonaws.com/recommender:latest
   ```

### Step 2: Deploy the Model to SageMaker
Run the provided deployment script (`deploy_sagemaker.py`) to create the model, endpoint configuration, and endpoint:

```bash
python deploy_sagemaker.py
```

---

## Testing the Endpoint

After the endpoint is deployed, test it using the following script:

```python
import boto3
import json

# Initialize SageMaker runtime client
runtime_client = boto3.client('sagemaker-runtime', region_name='us-east-1')

# Define input payload
payload = {
    "user_id": 1059637,
    "num_recommendations": 5
}

# Make a POST request to the endpoint
response = runtime_client.invoke_endpoint(
    EndpointName="recommender-endpoint-4",  # Replace with your endpoint name
    ContentType="application/json",
    Body=json.dumps(payload)
)

# Parse and print the response
result = json.loads(response['Body'].read().decode())
print(result)
```

---

## Troubleshooting

### Common Issues
1. **Error: `exec format error`**
   - Ensure the Docker image matches the architecture (`linux/amd64`) of the SageMaker instance.

2. **Error: `Endpoint not InService`**
   - Check the endpoint status in the AWS SageMaker console and ensure the logs do not have errors.

3. **Error: `Access Denied`**
   - Ensure the SageMaker execution role has the required permissions.

### Logs
To debug issues, check the CloudWatch logs for the endpoint in the SageMaker console.

---

