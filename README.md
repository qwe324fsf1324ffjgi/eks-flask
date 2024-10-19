Create a User
flask-user
Access Key : 
Secret Access Key : 

Create a new S3 bucket and upload your model files (deploy.prototxt and mobilenet_iter_73000.caffemodel
flask-cv-app

In your project root directory, create a file named Dockerfile with the following content:
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
FROM python:3.9-slim

# Install dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Set the working directory
WORKDIR /app

# Copy the app files into the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port the app will run on
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]




Create a requirements.txt file with Flask, OpenCV, and other dependencies:
Flask
opencv-python
numpy



Build the Docker image:
docker build -t flask-object-detection .


Run the image locally to test it:
docker run -p 5000:5000 flask-object-detection


Create ECR 
Repo Name: flask-app
241533154996.dkr.ecr.us-east-1.amazonaws.com/flask-app

CLI Command
aws configure 

Login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 241533154996.dkr.ecr.us-east-1.amazonaws.com

Tag the image
docker tag flask-object-detection:latest 241533154996.dkr.ecr.us-east-1.amazonaws.com/flask-app:latest


Push the image to ECR
docker push 241533154996.dkr.ecr.us-east-1.amazonaws.com/flask-app:latest


Install AWS Cli 
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

Download and install kubectl
https://dl.k8s.io/release/v1.26.0/bin/windows/amd64/kubectl.exe

Move kubectl to Program Files: After opening PowerShell with administrative privileges, try running the command to move kubectl.exe again:
Move-Item -Path "C:\Users\gauravja\Downloads\kubectl.exe" -Destination "C:\Program Files\kubectl.exe"

Add the Directory to Your PATH:

Right-click on This PC or My Computer on your desktop or in File Explorer.
Select Properties.
Click on Advanced system settings.
Click on the Environment Variables button.
In the System variables section, find the Path variable and click Edit.
Click New and add C:\Users\gauravja\bin.
Click OK to close all dialog boxes.

kubectl version --client


Download and install eksctl through Powershell
choco install eksctl

verify installation
eksctl version

Create an EKS Cluster: Create a cluster using eksctl
eksctl create cluster --name flask-cluster --version 1.30 --region us-east-1 --nodegroup-name linux-nodes --node-type t3.medium --nodes 3 --nodes-min 1 --nodes-max 4 --managed


Verify Cluster Setup: Once the cluster is ready, verify it using:
kubectl get svc

Deploy Flask App on Kubernetes
Create Kubernetes Deployment YAML:
Create a deployment.yaml file to define how your app will be deployed.

Create Kubernetes Service YAML:
Create a service.yaml file to expose the application.

Deploy the Application: Apply the deployment and service configuration:
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml


Check the Status: Check if the pods are running:
kubectl get pods

Get the External IP: Get the external IP of the LoadBalancer to access your app:
kubectl get svc flask-object-detection
