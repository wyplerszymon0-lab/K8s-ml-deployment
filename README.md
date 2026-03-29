# k8s-ml-deployment

A production-ready ML model deployment on Kubernetes. Exposes a trained scikit-learn classifier via a REST API, containerized with Docker and orchestrated with Kubernetes.

## Architecture
```
          ┌─────────────────────────────────────────┐
          │            Kubernetes Cluster            │
          │                                          │
          │   ┌──────────┐      ┌──────────────┐    │
Request ──┼──►│ Service  │─────►│     Pod 1    │    │
          │   │(LoadBal.)│      │  Flask + ML  │    │
          │   │          │      ├──────────────┤    │
          │   │          │─────►│     Pod 2    │    │
          │   └──────────┘      │  Flask + ML  │    │
          │        ▲            └──────────────┘    │
          │        │                   ▲            │
          │   ┌────┴─────┐             │            │
          │   │   HPA    │─────────────┘            │
          │   │(autoscale│  scales 2–10 pods        │
          │   └──────────┘  based on CPU usage      │
          └─────────────────────────────────────────┘
```

## Stack

- **Model**: Random Forest Classifier (scikit-learn) trained on Iris dataset
- **API**: Flask + Gunicorn
- **Container**: Docker (python:3.11-slim)
- **Orchestration**: Kubernetes (Deployment, Service, HPA)

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/predict` | Run inference |

### Example request
```bash
curl -X POST http://localhost/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

### Example response
```json
{
  "prediction": {
    "class_index": 0,
    "class_name": "setosa",
    "confidence": 0.97
  }
}
```

## Running locally with Docker
```bash
docker build -t ml-classifier .
docker run -p 5000:5000 ml-classifier
```

## Deploying to Kubernetes
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
```

Check status:
```bash
kubectl get pods
kubectl get svc
kubectl get hpa
```

## Project structure
```
k8s-ml-deployment/
├── app/
│   └── main.py           
├── model/
│   ├── __init__.py
│   └── classifier.py     
├── k8s/
│   ├── deployment.yaml   
│   ├── service.yaml      
│   └── hpa.yaml          
├── Dockerfile
└── requirements.txt
```

## Key concepts demonstrated

- **Containerization**: Docker image with slim base
- **Horizontal scaling**: HPA auto-scales pods based on CPU (2–10 replicas)
- **Health checks**: Liveness and readiness probes for zero-downtime deployments
- **Resource limits**: CPU and memory requests/limits per pod
- **REST inference**: Stateless prediction endpoint ready for production traffic
