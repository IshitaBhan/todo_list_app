README for Scalable To-Do List Application Deployment on Kubernetes
This repository contains all the necessary files to deploy and manage a scalable To-Do List web application using Kubernetes. The application is containerized using Docker and deployed on a Kubernetes cluster. It supports features like auto-scaling, rolling updates, persistent storage, logging, and self-healing.

Project Overview
The To-Do List web application is built using Python Flask and provides the following APIs:

GET /tasks: Retrieve all tasks.

POST /tasks: Add a new task.

DELETE /tasks/<task_id>: Delete a task by ID.

This project is designed to meet the following requirements:

Deploy a web application using Kubernetes with at least 3 replicas.

Implement Horizontal Pod Autoscaler (HPA) for scaling based on CPU usage.

Use ConfigMaps and Secrets for environment variables and sensitive data.

Simulate rolling updates and rollbacks.

Implement persistent storage (optional).

Test application availability, scaling, rolling updates, self-healing, persistent storage, and logging.

Folder Structure
text
todo-list-app/
├── app/
│   ├── app.py             # Python Flask application code
│   ├── requirements.txt   # Dependencies for Flask
├── docker/
│   └── Dockerfile         # Docker configuration
├── manifests/
│   ├── deployment.yaml    # Deployment configuration
│   ├── service.yaml       # Service configuration
│   ├── configmap.yaml     # ConfigMap for environment variables
│   ├── secret.yaml        # Secret for sensitive data
│   ├── hpa.yaml           # Horizontal Pod Autoscaler configuration
│   ├── pvc.yaml           # Persistent Volume Claim configuration
├── README.md              # Project documentation
Prerequisites
Tools Required:

Docker

Kubernetes CLI (kubectl)

Google Cloud SDK (for GKE) or Minikube (for local deployment)

Environment Setup:

A Kubernetes cluster with at least 2 worker nodes.

Metrics Server enabled for auto-scaling.

Steps to Deploy
Step 1: Build and Push Docker Image
Build the Docker image locally:

bash
docker build -t gcr.io/<PROJECT_ID>/todo-app:v1 -f docker/Dockerfile .
Replace <PROJECT_ID> with your Google Cloud Project ID.

Push the image to Google Artifact Registry or Docker Hub:

bash
docker push gcr.io/<PROJECT_ID>/todo-app:v1
Step 2: Deploy Kubernetes Resources
Navigate to the manifests/ directory where all YAML files are stored.

Apply the ConfigMap:

bash
kubectl apply -f configmap.yaml
Apply the Secret:

bash
kubectl apply -f secret.yaml
Apply the Deployment:

bash
kubectl apply -f deployment.yaml
Apply the Service:

bash
kubectl apply -f service.yaml
Verify that pods are running:

bash
kubectl get pods -w
Get the external IP of the service:

bash
kubectl get services todo-app-service
Access your application at http://<EXTERNAL-IP>.

Step 3: Configure Horizontal Pod Autoscaler (HPA)
Apply the HPA manifest:

bash
kubectl apply -f hpa.yaml
Monitor HPA scaling behavior:

bash
kubectl get hpa -w
Step 4: Persistent Storage Setup (Optional)
Apply Persistent Volume Claim (PVC):

bash
kubectl apply -f pvc.yaml
Update deployment.yaml to include PVC configuration, then reapply it:

bash
kubectl apply -f deployment.yaml
Step 5: Rolling Updates and Rollbacks
Rolling Update:
Update the image in deployment.yaml to a new version (e.g., todo-app:v2) and reapply it:

bash
kubectl set image deployment/todo-app todo-app-container=gcr.io/<PROJECT_ID>/todo-app:v2 --record=true 
Monitor rollout status:

bash
kubectl rollout status deployment/todo-app 
Rollback:
If there’s an issue with the new version, rollback to the previous version:

bash
kubectl rollout undo deployment/todo-app --to-revision=1 
Testing Scenarios
1. Application Availability Test
Check if the application is accessible via the Kubernetes service:

bash
curl http://<EXTERNAL-IP>
Expected Output: "Welcome to the To-Do List App!".

2. Scaling Test
Trigger high CPU usage to test Horizontal Pod Autoscaler (HPA):

Run a temporary pod for stress testing:

bash
kubectl run --rm -it load-generator --image=busybox -- /bin/sh -c "while true; do wget -q -O- http://<SERVICE-IP>; done"
Monitor HPA scaling behavior:

bash
kubectl get hpa -w 
kubectl get pods -w 
Expected Output: Number of pods should increase dynamically.

3. Rolling Update & Rollback Test
Perform a rolling update and verify zero downtime:

Update deployment image:

bash
kubectl set image deployment/todo-app todo-app-container=gcr.io/<PROJECT_ID>/todo-app:v2 --record=true 
Rollback if needed:

bash
kubectl rollout undo deployment/todo-app 
Expected Output: Application reverts to the previous working version.

4. Pod Failure and Self-Healing Test
Manually delete a pod and check if Kubernetes automatically recreates it:

bash
kubectl delete pod <POD_NAME> 
Verify that a new pod is created automatically:

bash
kubectl get pods -w 
Expected Output: A new pod should be automatically created.

5. Persistent Storage Test
Verify if data persists after pod restart:

Access a running pod and store data in /data volume:

bash
kubectl exec -it <POD_NAME> -- /bin/bash 
echo "Test Data" > /data/test-file.txt 
exit 
Delete the pod manually:

bash
kubectl delete pod <POD_NAME> 
Access a newly created pod and check if data persists:

bash
kubectl exec -it <NEW_POD_NAME> -- /bin/bash 
cat /data/test-file.txt 
Expected Output: "Test Data".

6. Logging Test
View logs of a specific pod:

bash
kubectl logs <POD_NAME> 
Expected Output: Logs from the application showing API requests/responses.

Deliverables Checklist
 Dockerfile for containerizing the application.

 Kubernetes YAML manifests (deployment.yaml, service.yaml, hpa.yaml, etc.).

 Step-by-step README.md with setup instructions.

 Screenshots of running cluster and auto-scaling in action.

 Test Cases for all 6 tests done above.

Notes
This repository is designed to meet all assignment requirements for deploying and managing a scalable web application using Kubernetes. It includes features like auto-scaling, rolling updates/rollback, persistent storage, logging, and self-healing mechanisms.