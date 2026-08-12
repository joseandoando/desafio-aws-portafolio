# Jose Calfullan — Cloud / DevOps / SRE Engineering Portfolio

Hands-on engineering portfolio focused on **AWS, Linux, Infrastructure as Code, CI/CD, observability, automation and production reliability**.

[![SRE Observability Lab](https://github.com/joseandoando/desafio-aws-portafolio/actions/workflows/sre-observability-lab.yml/badge.svg)](https://github.com/joseandoando/desafio-aws-portafolio/actions/workflows/sre-observability-lab.yml)
[![AWS Data Pipeline](https://github.com/joseandoando/desafio-aws-portafolio/actions/workflows/aws-data-pipeline-floci.yml/badge.svg)](https://github.com/joseandoando/desafio-aws-portafolio/actions/workflows/aws-data-pipeline-floci.yml)

## About me

Telecommunications and infrastructure engineer with professional experience in **SOC/NOC operations, Linux systems, cloud infrastructure, monitoring, incident response and network/security operations**.

My current technical focus is moving deeper into **DevOps, Site Reliability Engineering and AWS Cloud Engineering**, building projects that demonstrate production-style engineering practices instead of only listing technologies on a CV.

### Certifications

- AWS Certified Solutions Architect — Associate
- AWS Certified Cloud Practitioner
- Fortinet NSE 4 — FortiOS 7.6 Administrator
- Google Cybersecurity Professional Certificate
- Cisco Cybersecurity / Network Defense training

## Featured engineering labs

### 1. SRE / DevOps Observability Lab

**[Open project →](labs/sre-observability-lab/)**

Production-oriented reliability lab built around a small observable service and a reproducible AWS architecture.

**Stack:** `AWS ECS Fargate` · `ALB` · `CloudWatch` · `Terraform` · `Docker` · `Prometheus` · `Grafana` · `Python` · `Bash` · `GitHub Actions`

**What it demonstrates:**

- Health and readiness checks
- Prometheus application metrics
- Error-rate and p95 latency alerts
- SLI/SLO and error-budget concepts
- P0/P1 incident response runbook
- Docker-based local observability stack
- AWS ECS/Fargate architecture with ALB
- CloudWatch Logs, Container Insights and alarms
- Terraform Infrastructure as Code
- Automated smoke testing in CI

### 2. AWS Data Engineering Lab

**[Open project →](labs/aws-data-pipeline/)**

AWS-oriented data pipeline with an executable local AWS-compatible path for integration testing without cloud cost.

**Stack:** `Amazon S3` · `AWS Glue` · `Athena` · `PySpark` · `Parquet` · `Python/Boto3` · `Terraform` · `Docker` · `GitHub Actions`

```text
CSV -> S3 raw -> PySpark -> S3 curated (Parquet) -> Glue Data Catalog -> Athena
```

**What it demonstrates:**

- Python/Boto3 ingestion
- S3 raw/curated data-lake pattern
- Glue Data Catalog
- PySpark ETL
- Parquet transformation
- Athena SQL analytics
- Terraform infrastructure definitions
- Docker-based integration testing
- GitHub Actions CI

## DevOps / SRE skills demonstrated

| Area | Technologies / Practices |
|---|---|
| Cloud | AWS, ECS Fargate, S3, IAM, VPC, ALB, CloudWatch |
| Infrastructure as Code | Terraform |
| Containers | Docker, Docker Compose, ECS |
| CI/CD | GitHub Actions, automated validation and integration tests |
| Observability | Prometheus, Grafana, CloudWatch, metrics, alerting |
| Reliability | SLI, SLO, error budgets, health checks, incident response |
| Automation | Python, Bash, Boto3 |
| Systems | Linux, networking, troubleshooting |
| Data / Cloud | Glue, Athena, PySpark, Parquet |

## Engineering approach

1. **Automate repeatable work.** Infrastructure and validation should be reproducible.
2. **Observe before guessing.** Metrics, logs and health signals drive troubleshooting.
3. **Design for failure.** Reliability includes detection, mitigation, rollback and post-incident learning.
4. **Validate in CI.** Infrastructure and application changes should be checked before deployment.
5. **Be explicit about scope.** Local AWS-compatible simulations are documented as simulations and are not presented as real production deployments.
6. **Keep cloud cost controlled.** CI validates infrastructure without automatically provisioning billable AWS resources.

## Repository structure

```text
.
├── .github/workflows/
│   ├── sre-observability-lab.yml
│   └── aws-data-pipeline-floci.yml
└── labs/
    ├── README.md
    ├── sre-observability-lab/
    └── aws-data-pipeline/
```

## Current focus

- AWS production operations
- Terraform modules and reusable infrastructure
- CI/CD deployment strategies
- ECS and Kubernetes
- CloudWatch and observability
- SLO-based alerting
- Incident response automation
- Infrastructure troubleshooting

## Contact

- **LinkedIn:** [Jose Calfullan](https://linkedin.com/in/jose-calfullan-00b9362a5)
- **GitHub:** [@joseandoando](https://github.com/joseandoando)

---

> This repository started as an AWS portfolio challenge and has evolved into a practical Cloud / DevOps / SRE engineering portfolio.
