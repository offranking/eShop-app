# My E-Shop Application
This is a simple Flask-based e-shop web application designed for deployment using Docker and managed via Azure Kubernetes Service (AKS). The app is integrated with Azure DevOps CI/CD pipeline for automated build and deployment.

## Project Overview
This application serves as a simple e-shop platform. The backend is powered by Flask, and the frontend is served via HTML templates. The application is packaged into a Docker container and deployed to Azure Kubernetes Service (AKS). The CI/CD pipeline, managed through Azure DevOps, automates the build and deployment process to Azure.

## Technologies Used
Flask: Python web framework for building the e-shop application.

Docker: Containerizes the application to ensure consistent environment across different stages.

Azure DevOps: Used for automating the build and deployment process.

Azure Kubernetes Service (AKS): Hosts the application in a scalable and managed Kubernetes environment.

Kubernetes: Manages deployment, scaling, and operations of the application container.

Azure Container Registry (ACR): Stores Docker images built from the application code.

## Project Structure

```
my-eshop/
├── app.py               # Flask application entry point
├── templates/           # HTML files
│   ├── index.html
│   ├── goods.html
│   └── services.html
├── Dockerfile           # Docker configuration for the app
├── kubernetes-manifest.yml  # Kubernetes deployment and service configuration
├── azure-pipelines.yml  # Azure DevOps pipeline configuration
└── requirements.txt     # Python dependencies
```

## Flask Application (app.py)
The app.py file is the core of the application. It defines the routes for the homepage, goods, and services pages.

```
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/goods')
def goods():
    return render_template('goods.html', title='Goods')

@app.route('/services')
def services():
    return render_template('services.html', title='Services')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## Kubernetes Manifest (kubernetes-manifest.yml)
This file contains the Kubernetes deployment and service configuration to deploy the app on Azure Kubernetes Service (AKS).

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-eshop-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-eshop
  template:
    metadata:
      labels:
        app: my-eshop
    spec:
      containers:
      - name: my-eshop-container
        image: udodevprojectacr.azurecr.io/my-eshop:$(Build.BuildId)
        ports:
        - containerPort: 5000

---

apiVersion: v1
kind: Service
metadata:
  name: my-eshop-service
spec:
  selector:
    app: my-eshop
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
```

## Dockerfile
This Dockerfile builds the image for the application and sets it up to run on a container.

```
# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory content into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to the host
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
```

# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory content into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 to the host
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]

## Azure DevOps Pipeline (azure-pipelines.yml)
This pipeline automates the process of building the Docker image, pushing it to Azure Container Registry (ACR), and deploying it to Azure Kubernetes Service (AKS).


```
trigger:
- main

pr:
- main

jobs:
- job: Build
  displayName: 'Build and Push to ACR'
  pool:
    vmImage: 'ubuntu-latest'
  steps:
  - checkout: self
  - task: UsePythonVersion@0
    inputs:
      versionSpec: '3.x'
  - script: |
      docker build -t $(Build.Repository.Name):$(Build.BuildId) .
      docker tag $(Build.Repository.Name):$(Build.BuildId) udodevprojectacr.azurecr.io/my-eshop:$(Build.BuildId)
      echo "$(acrPassword)" | docker login udodevprojectacr.azurecr.io -u $(acrUsername) --password-stdin
      docker push udodevprojectacr.azurecr.io/my-eshop:$(Build.BuildId)
    displayName: 'Build and Push'

- deployment: DeployToAKS
  displayName: 'Deploy to AKS'
  dependsOn: Build
  pool:
    vmImage: 'ubuntu-latest'
  environment: 'udodevprojectaks'
  strategy:
    runOnce:
      deploy:
        steps:
        - checkout: self
        - task: UsePythonVersion@0
          inputs:
            versionSpec: '3.x'
        - script: |
            kubectl apply -f kubernetes-manifest.yml
          displayName: 'Deploy to AKS'
```



