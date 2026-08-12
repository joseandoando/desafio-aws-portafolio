# SRE / DevOps Observability Lab

Production-oriented lab built to demonstrate practical Site Reliability Engineering and DevOps skills: containerization, observability, alerting, SLOs, incident response, AWS infrastructure as code and CI validation.

## What this project demonstrates

- Docker and Docker Compose
- Python service with health/readiness endpoints
- Prometheus metrics and alert rules
- Grafana-ready local observability stack
- SLI/SLO definition and error-budget thinking
- P0/P1-style incident triage runbook
- Terraform Infrastructure as Code
- AWS ECS Fargate, ALB, IAM and VPC networking
- AWS CloudWatch Logs, Container Insights and alarms
- GitHub Actions CI
- Bash smoke testing and operational automation

## Architecture

### Local reliability lab

```text
             +----------------+
             |   Test / User  |
             +-------+--------+
                     |
                     v
             +----------------+
             | Python Service |
             | :8080          |
             +-------+--------+
                     |
        /metrics     |
                     v
             +----------------+
             |   Prometheus   |
             | :9090          |
             +-------+--------+
                     |
                     v
             +----------------+
             |    Grafana     |
             | :3000          |
             +----------------+
```

### AWS design

```text
Internet
   |
   v
Application Load Balancer
   |
   +-------------------+
   |                   |
   v                   v
ECS Fargate Task   ECS Fargate Task
   |                   |
   +---------+---------+
             |
             v
      CloudWatch Logs
      Container Insights
      CloudWatch Alarms
```

Terraform creates a VPC, two availability-zone subnets, security groups, an Application Load Balancer, ECS Fargate service, IAM execution role, CloudWatch log group and operational alarms.

## Reliability signals

The service exposes:

| Endpoint | Purpose |
|---|---|
| `/health` | Liveness / service health |
| `/ready` | Readiness check |
| `/metrics` | Prometheus metrics |
| `/simulate/error` | Controlled HTTP 500 for alert testing |
| `/simulate/latency` | Controlled slow request for latency testing |

Primary metrics:

- `demo_http_requests_total`
- `demo_http_request_duration_seconds`

Alert examples:

- Error ratio above 5% for 2 minutes
- p95 latency above 500 ms for 5 minutes

See [`docs/SLO.md`](docs/SLO.md) for the SLI/SLO model and [`docs/RUNBOOK.md`](docs/RUNBOOK.md) for incident response.

## Run locally

Requirements:

- Docker
- Docker Compose
- curl

```bash
cd labs/sre-observability-lab
docker compose up -d --build
bash scripts/smoke_test.sh
```

Open:

- App: `http://localhost:8080`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

Generate reliability signals:

```bash
curl http://localhost:8080/simulate/error
curl http://localhost:8080/simulate/latency
```

Stop the lab:

```bash
docker compose down -v
```

## AWS / Terraform

The AWS module is intentionally not auto-applied by CI because a real deployment creates billable resources.

Build and push the app image to ECR, then provide the image URI:

```bash
cd terraform
terraform init
terraform plan -var='container_image=<account>.dkr.ecr.<region>.amazonaws.com/sre-demo:latest'
```

For an actual deployment:

```bash
terraform apply -var='container_image=<account>.dkr.ecr.<region>.amazonaws.com/sre-demo:latest'
```

The repository validates Terraform syntax in GitHub Actions without provisioning cloud resources.

## CI pipeline

`.github/workflows/sre-observability-lab.yml` executes two independent checks:

1. **Terraform validation**: format, init without backend and validate.
2. **Local SRE integration test**: builds the container, starts Prometheus/Grafana, validates health/readiness/metrics, generates controlled error and latency events, and checks Prometheus readiness.

## Incident response scenario

A simple interview/demo exercise:

1. Start the stack.
2. Generate repeated `/simulate/error` requests.
3. Observe the 5xx metric in Prometheus.
4. Review the `HighErrorRate` alert rule.
5. Follow the runbook to triage impact and likely causes.
6. Explain how the same workflow maps to ECS, CloudWatch and a production on-call process.

## Production improvements

For a real production environment I would extend this design with:

- Private ECS subnets and NAT/VPC endpoints
- HTTPS with ACM
- ECR image scanning
- Secrets Manager / Parameter Store
- ECS autoscaling based on service metrics
- CloudWatch or Datadog distributed tracing
- Multi-window error-budget burn-rate alerts
- Remote Terraform state with S3 and DynamoDB locking
- Blue/green or canary deployment strategy
- Automated rollback based on health and SLO degradation

## Interview talking points

- Difference between monitoring and observability
- Why liveness and readiness checks have different purposes
- How to choose an SLI and turn it into an SLO
- Why alerting should be tied to customer impact and error-budget burn
- First actions during a P0/P1 production incident
- When to mitigate/rollback before investigating root cause
- How Terraform improves repeatability and reviewability
- How ECS/Fargate changes operational responsibility compared with EC2
- Why CI validates infrastructure but does not automatically apply production changes
