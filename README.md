# Code Review MCP is a Proof of Concept (PoC) that simulates the behaviour of a Model Context Protocol (MCP) system for automated code review.
It uses FastAPI to expose a simple HTTP interface that communicates with Azure OpenAI models (such as gpt-4o-mini-2) to analyse Merge Request (MR) diffs and provide intelligent review comments.

# How It Works

The FastAPI service accepts MR diffs or code snippets via an API endpoint.
It constructs a prompt to send to the Azure OpenAI model for contextual code analysis.
The model responds with review suggestions, which are returned as structured JSON output.
This mimics the MCP-style interaction between a client (e.g., GitLab MR) and a review agent without using the official MCP SDK.

# Purpose
This PoC is designed to:

Explore how LLMs can automate MR code reviews.
Validate communication between FastAPI services and Azure OpenAI endpoints.
Provide a foundation for a future production-grade MCP-based system with improved context handling, guardrails, and scalability.

# Future Roadmap — Full MCP Server Integration

This PoC is the foundation for a scalable, production-grade AI Code Review Assistant that will leverage the Model Context Protocol (MCP) architecture for deeper integration and automation.

## Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Running Locally](#running-locally)  
5. [Kubernetes Deployment](#kubernetes-deployment)  
6. [Environment Variables & Secrets](#environment-variables--secrets)  
7. [API Usage](#api-usage)  
8. [Sample Test](#sample-test)  
9. [Troubleshooting](#troubleshooting)  
10. [Contributing](#contributing)  
11. [License](#license)  

---

## Features

- Review Merge Requests automatically using Azure OpenAI.
- Detects code issues, typos, and provides suggestions.
- REST API endpoint for integration with other tools.
- Can run locally or in Kubernetes.

---

## Prerequisites

- Python 3.11+
- Docker (optional for containerization)
- Kubernetes cluster (for deployment i.e. local setup using minikube)
- Azure OpenAI subscription and deployed model
- `kubectl` and Helm installed if deploying to Kubernetes

---

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd <repo-directory>
```

2. Create a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables & Secrets

This project requires the following environment variables. Store them in a `.env` file at the root of your project:

```dotenv
# .env file

# Your Azure OpenAI API key
AZURE_OPENAI_KEY=your_azure_openai_key_here

# Your Azure OpenAI endpoint URL
AZURE_OPENAI_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/

# The deployed model name in Azure OpenAI
MODEL_NAME=gpt-4o-mini-2
```

## Running Locally

Start the FastAPI application:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Access the API:

- Health check: [http://localhost:8080/health](http://localhost:8080/health)

---

## Kubernetes Deployment

1. Build Docker image:

```bash
docker build -t code-review-mcp:latest .
```

2. Push to container registry (optional):

```bash
docker tag code-review-mcp:latest <registry-url>/code-review-mcp:latest
docker push <registry-url>/code-review-mcp:latest
```

3. Deploy using Helm:

```bash
# Create or overwrite helm/values.yaml with the required configuration

cat <<EOF > helm/values.yaml
image:
  repository: image.registry.com/code-review-mcp
  tag: latest

service:
  port: 8000

azureOpenAI:
  endpoint: "https://your-azure-openai-endpoint.openai.azure.com/"
  key: "your-azure-openai-key"
  model_name: "gpt-4o-mini-2"
EOF
```

```bash
helm install code-review-mcp ./helm-chart -n ai-review --create-namespace
```

4. Verify pod status:

```bash
kubectl get pods -n ai-review
kubectl logs -f pod/<pod-name> -n ai-review
```

---

---

## Sample Test

Run the following `curl` command to test locally:

```bash
curl -X POST http://localhost:8080/mcp/tool-call \
-H "Content-Type: application/json" \
-d '{"tool":"review_merge_request","arguments":{"diff":"print(\"prinf(hello)\")"}}'
```

```bash
### Merge Request Review Summary

It looks like you've shared a line from a GitLab Merge Request (MR) diff.  
In the code snippet, there's a small typo in the `print` function — it’s incorrectly written as `prinf`.

### **Suggested Change**

print("hello")

```

---

## Troubleshooting

- **SSL Issues with Azure OpenAI:**  
  Make sure the pod or local machine can reach the Azure endpoint. For Kubernetes, consider using host networking or check firewall rules.

- **Internal Server Error (500):**  
  Check logs:  
  ```bash
  kubectl logs -f pod/<pod-name> -n ai-review
  ```
  Ensure that environment variables are correctly set and loaded.

- **Curl connection fails:**  
  Verify network connectivity to `*.cognitiveservices.azure.com`.

---

## Contributing

- Fork the repository
- Create a feature branch: `git checkout -b feature/my-feature`
- Commit changes: `git commit -m 'Add new feature'`
- Push branch: `git push origin feature/my-feature`
- Open a Pull Request
