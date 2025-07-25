


# 🚀 AutoPaaS-X

**AutoPaaS-X** is a self-learning, AI-driven Platform-as-a-Service (PaaS) orchestrator that intelligently provisions, scales, and manages applications based on real-time workload, historical usage, and infrastructure constraints.

> Built using Python, Flask, TensorFlow, Q-Learning, Kubernetes, and OpenDaylight SDN.

---

## 📌 Features

- ✅ **LSTM-based resource predictor** (CPU, RAM)
- ✅ **Q-Learning engine** for dynamic scaling decisions
- ✅ **Dependency mediator** to resolve Python package conflicts
- ✅ **Serverless CronJob generator** to eliminate cold starts
- ✅ **SDN-based bandwidth throttler** using OpenDaylight
- ✅ **Feedback loop** for continuous learning
- ✅ **Kubernetes deployment integration**
- ✅ Fully modular architecture via RESTful Flask APIs

---

## 📁 Folder Structure

```

AutoPaaS-X/
├── ai/                    # AI models: LSTM predictor, Q-Learning, dependency checker
│   ├── lstm\_predictor.py
│   ├── q\_learning.py
│   └── dependency\_mediator.py
├── serverless/            # CronJob generator
│   └── cronjob\_generator.py
├── sdn/                   # Bandwidth throttling logic
│   └── throttler.py
├── scheduler/             # (Planned) solar-aware scheduler
├── api/                   # Flask API controller
│   └── paas\_controller.py
├── manifests/             # Generated CronJob / K8s YAMLs
├── test\_\*.py              # Independent test scripts
├── requirements.txt       # Python dependencies
├── Dockerfile             # (optional) Flask container
└── README.md              # You're reading it!

````

---

## ⚙️ Setup Instructions

### ✅ 1. Clone and Set Up Virtual Environment

```bash
git clone https://github.com/Janani2405/AutoPaaS-X.git
cd AutoPaaS-X
python -m venv venv
.\venv\Scripts\activate       # Windows
# source venv/bin/activate    # Linux/Mac
pip install -r requirements.txt
````

---

### ✅ 2. Run the Flask API Server

```bash
python -m api.paas_controller
```

* The API will run at: `http://localhost:5000`

---

## 🎯 Usage Examples

### 🔁 POST `/deploy_application`

Unified endpoint that:

* Predicts CPU/RAM
* Fixes `requirements.txt`
* Generates CronJob
* Applies K8s deployment
* Evaluates bandwidth fairness

#### 🧪 Sample JSON Payload:

```json
{
  "os": 1,
  "arch": 64,
  "image_size": 12,
  "feature": 1,
  "users": 100,
  "usage_hours": 6.0,
  "historical_usage": 80.0,
  "requirements": ["tensorflow==2.9.0", "flask==2.1.0"],
  "function_name": "data-cleaner",
  "invocation_times": ["09:00", "09:30", "10:00"],
  "tenant_bandwidth": {
    "tenant1": 3.5,
    "tenant2": 2.1,
    "tenant3": 8.9,
    "tenant4": 1.0
  }
}
```

✅ Response:

```json
{
  "status": "Deployed successfully",
  "predicted_resources": {
    "predicted_cpu_units": 2.19,
    "predicted_ram_MB": 512
  },
  "cleaned_requirements": [
    "tensorflow==2.12.0",
    "flask==2.1.0"
  ]
}
```

---

## ⚙️ API Reference

| Endpoint                | Method | Description                               |
| ----------------------- | ------ | ----------------------------------------- |
| `/predict_resources`    | POST   | Predict CPU & RAM based on input features |
| `/resolve_dependencies` | POST   | Sanitize Python package versions          |
| `/generate_cronjob`     | POST   | Generate warm-up CronJob for serverless   |
| `/enforce_bandwidth`    | POST   | Detect and throttle over-usage tenants    |
| `/feedback/resource`    | POST   | Update Q-table with performance feedback  |
| `/deploy_application`   | POST   | 🔥 Full orchestration pipeline            |

---

## 🧠 Learning Models

* LSTM predicts:

  * CPU (cores)
  * RAM (MB)
* Q-learning decides:

  * When to scale up / down / hold
* Bandwidth policy:

  * Throttle if tenant usage > 2× median
* Feedback:

  * Bad performance → penalty → smarter next time

---

## ☸️ Kubernetes Integration

Make sure Minikube or your cluster is running:

```bash
minikube start
kubectl get nodes
```

Then deploy a generated YAML:

```bash
python test_k8s_deploy.py
```

Or:

```bash
kubectl apply -f manifests/your_app_deployment.yaml
```

---

## 🐳 Optional Docker Support

To build a container:

### 📄 `Dockerfile`

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "-m", "api.paas_controller"]
```

### 📦 Build and Run

```bash
docker build -t autopaas .
docker run -p 5000:5000 autopaas
```

---

## 👩‍💻 Developed by

**Janani A**
B.Tech IT | Cloud & AI Enthusiast

> Project: Academic + Cloud Lab Use

---

## 📜 License

MIT License (optional — add if needed)

---

