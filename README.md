# Summarizer API

A production-grade text summarization API powered by LLMs (Groq), built with FastAPI, and served behind an Nginx load balancer.

## Features

- Text summarization via Groq LLM
- SQLAlchemy-backed request history
- Nginx reverse-proxy with two app replicas
- Containerized with Docker

## Local Development

### Prerequisites

- Docker & Docker Compose
- A [Groq API key](https://console.groq.com/)

### Setup

```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
docker-compose up --build
```

The API will be available at `http://localhost:80`.

### Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Deploying to AWS

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that automatically builds and deploys the Docker image to **Amazon ECS (Fargate)** on every push to `main`.

### AWS Prerequisites

1. **ECR repository** – Create a repository named `summarizer-api` in Amazon ECR.
2. **ECS cluster** – Create a cluster named `summarizer-cluster`.
3. **ECS task definition** – Register a task definition named `summarizer-api` with a container also named `summarizer-api` that exposes port `8000`. Add `GROQ_API_KEY` as an environment variable (or reference it from AWS Secrets Manager).
4. **ECS service** – Create a service named `summarizer-service` inside the cluster, using the task definition above.

### GitHub Secrets

Add the following secrets to your GitHub repository (**Settings → Secrets and variables → Actions**):

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key with ECS/ECR permissions |
| `AWS_SECRET_ACCESS_KEY` | Corresponding IAM secret key |
| `GROQ_API_KEY` | Your Groq API key (used by the CI test job) |

The IAM user needs at minimum the following permissions:
- `ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, `ecr:PutImage`, `ecr:InitiateLayerUpload`, `ecr:UploadLayerPart`, `ecr:CompleteLayerUpload`
- `ecs:RegisterTaskDefinition`, `ecs:DescribeTaskDefinition`, `ecs:UpdateService`, `ecs:DescribeServices`
- `iam:PassRole` (for the ECS task execution role)

### Deployment Flow

1. Push code to the `main` branch.
2. The **CI** workflow runs tests.
3. The **Deploy to AWS ECS** workflow:
   - Builds the Docker image.
   - Pushes it to Amazon ECR tagged with the commit SHA.
   - Updates the ECS task definition with the new image.
   - Deploys the updated task definition to the ECS service and waits for stability.

### Changing the AWS Region

The default region is `us-east-1`. To use a different region, update the `AWS_REGION` environment variable at the top of `.github/workflows/deploy.yml`.
