# AI DevOps Assignment

## Project Overview

This project demonstrates a production-style deployment of a containerized FastAPI application using Docker and AWS infrastructure.

The stack includes:

* FastAPI backend
* PostgreSQL database
* Redis cache
* NGINX reverse proxy
* Docker Compose orchestration
* GitHub Actions CI/CD pipeline
* AWS EC2 deployment
* AWS IAM Role integration
* AWS Secrets Manager integration

The goal of this assignment was to showcase practical DevOps deployment knowledge, infrastructure organization, CI/CD automation, and production-oriented architecture.

---

# GitHub Repository

```text id="v4x8mp"
Repository Name: fast-api-task
```

---

# Architecture

```text id="g8m2qw"
                    GitHub Repository
                            │
                            │ Push
                            ▼
                  GitHub Actions CI/CD
                            │
                            │ SSH Deployment
                            ▼
                  AWS EC2 Instance (Ubuntu)
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
         ▼                  ▼                  ▼
      FastAPI           PostgreSQL           Redis
         │
         ▼
      NGINX Reverse Proxy
         │
         ▼
      Public Access via Elastic IP
```

---

# Tech Stack

| Component         | Technology          |
| ----------------- | ------------------- |
| Backend API       | FastAPI             |
| Database          | PostgreSQL 16       |
| Cache             | Redis 7             |
| Reverse Proxy     | NGINX               |
| Containerization  | Docker              |
| Orchestration     | Docker Compose      |
| CI/CD             | GitHub Actions      |
| Cloud Provider    | AWS EC2             |
| Secret Management | AWS Secrets Manager |
| Authentication    | IAM Role            |

---

# Features Implemented

* Dockerized FastAPI application
* PostgreSQL integration
* Redis caching
* NGINX reverse proxy
* Health check endpoint
* Metrics endpoint
* CRUD APIs
* Persistent Docker volumes
* GitHub Actions deployment pipeline
* IAM Role based authentication
* AWS Secrets Manager integration
* Automatic container restart policies
* Container health checks
* Reverse proxy configuration

---

# Project Structure

```text id="t1m9zr"
fast-api-task/
│
├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── nginx/
│   └── default.conf
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── docker-compose.yml
├── secrets-loader.sh
└── README.md
```

---

# AWS Infrastructure Used

## EC2 Instance

* Ubuntu Server
* Elastic IP attached
* Docker installed
* GitHub Actions deployment target

## IAM Role

An IAM Role was attached to the EC2 instance to securely access AWS Secrets Manager without storing AWS access keys.

## AWS Secrets Manager

Application secrets are securely stored in AWS Secrets Manager and injected into Docker Compose runtime during deployment.

---

# Environment Variables

The following environment variables are used:

| Variable          | Purpose                  |
| ----------------- | ------------------------ |
| POSTGRES_DB       | PostgreSQL database name |
| POSTGRES_USER     | PostgreSQL username      |
| POSTGRES_PASSWORD | PostgreSQL password      |
| REDIS_HOST        | Redis hostname           |

Secrets are fetched dynamically using AWS CLI and injected into Docker Compose during deployment.

---

# Docker Compose Services

## FastAPI App

* Runs FastAPI backend
* Exposes port 8000 internally
* Connects to PostgreSQL and Redis

## PostgreSQL

* Persistent database storage
* Docker volume enabled

## Redis

* Used for caching API responses

## NGINX

* Reverse proxy for FastAPI
* Handles incoming HTTP traffic

---

# API Endpoints

| Method | Endpoint      | Description     |
| ------ | ------------- | --------------- |
| GET    | `/`           | Root endpoint   |
| GET    | `/health`     | Health check    |
| GET    | `/metrics`    | Service metrics |
| POST   | `/users`      | Create user     |
| GET    | `/users`      | Get users       |
| DELETE | `/users/{id}` | Delete user     |

---

# Redis Caching Demonstration

The `/users` endpoint demonstrates Redis caching.

## First Request

Data is fetched from PostgreSQL.

Response:

```json id="n8m2qx"
{
  "source": "postgresql"
}
```

## Subsequent Requests

Data is served from Redis cache.

Response:

```json id="q5x1wb"
{
  "source": "redis-cache"
}
```

---

# CI/CD Pipeline

GitHub Actions pipeline automatically:

1. Connects to EC2 using SSH
2. Pulls latest code
3. Fetches secrets from AWS Secrets Manager
4. Rebuilds Docker containers
5. Deploys updated services

---

# GitHub Actions Workflow

The deployment pipeline is located at:

```text id="u7m4zr"
.github/workflows/deploy.yml
```

Deployment is triggered automatically on push to the `main` branch.

---

# Health Checks

Docker health checks are configured for:

* FastAPI
* PostgreSQL
* Redis

Health endpoint:

```text id="j3q8nv"
/health
```

---

# Logging Strategy

Container logs can be viewed using:

```bash id="v9m1kr"
docker logs fastapi-app
docker logs postgres-db
docker logs redis-cache
docker logs nginx-proxy
```

For real production environments, centralized logging solutions such as:

* Grafana Loki
* ELK Stack
* CloudWatch Logs

can be integrated.

---

# Backup Strategy

## PostgreSQL Backup

Example backup command:

```bash id="w2x7mp"
docker exec postgres-db pg_dump -U admin appdb > backup.sql
```

## Future Improvements

* Automated S3 backups
* Scheduled cron backups
* Point-in-time recovery

---

# Restart Strategy

Docker restart policies are configured using:

```yaml id="p6m3zx"
restart: always
```

This ensures services restart automatically after:

* crashes
* EC2 reboot
* Docker daemon restart

---

# Security Measures

Implemented:

* IAM Role authentication
* AWS Secrets Manager integration
* Reverse proxy isolation
* Docker network isolation
* Secrets removed from repository
* GitHub Secrets for CI/CD

Recommended future improvements:

* HTTPS with domain-based SSL
* Fail2Ban
* UFW firewall hardening
* Cloudflare integration
* WAF protection

---

# SSL Approach

Initially explored:

* Let’s Encrypt IP-based SSL certificates

However, due to current limitations and instability of experimental IP-based ACME validation on cloud providers, production recommendation is to use:

* Domain-based SSL certificates
* Cloudflare
* Route53 + ACM

---

# Deployment Instructions

## Clone Repository

```bash id="k4m8wb"
git clone <repo-url>
cd fast-api-task
```

---

# Install Docker

```bash id="r1q9vx"
sudo apt update
sudo apt install docker.io docker-compose-plugin -y
```

---

# Start Application

```bash id="t7m2zr"
chmod +x secrets-loader.sh
./secrets-loader.sh
```

---

# Verify Running Containers

```bash id="h5x8mk"
docker compose ps
```

---

# Access Application

```text id="c9m1qp"
http://<EC2_ELASTIC_IP>
```

---

# Useful Commands

## View Logs

```bash id="m2q7wb"
docker logs fastapi-app
```

## Restart Stack

```bash id="x8m4nv"
docker compose restart
```

## Stop Stack

```bash id="p3q9zr"
docker compose down
```

## Remove Volumes

```bash id="w6m1kx"
docker compose down -v
```

---

# Future Improvements

* HTTPS with domain
* Kubernetes deployment
* Grafana monitoring
* Prometheus metrics
* Blue-Green deployment
* Zero-downtime deployments
* Auto-scaling
* Cloudflare integration

---

# Learning Outcomes

This project demonstrates understanding of:

* Docker containerization
* Reverse proxy configuration
* CI/CD automation
* AWS infrastructure
* IAM roles
* Secret management
* Application deployment
* Service orchestration
* Production debugging
* Infrastructure troubleshooting

---

Step By Step Implementation

Add this section in your README after the “Deployment Instructions” section.

---

# Step-by-Step Setup Guide

## 1. Launch EC2 Instance

* Create Ubuntu EC2 instance on AWS
* Attach Security Group with:

  * Port 22 (SSH)
  * Port 80 (HTTP)

Recommended instance type:

```text id="k7m2vx"
t2.micro
```

Attach an Elastic IP to keep public IP static.

---

# 2. Connect to EC2

```bash id="w4q8zr"
ssh -i your-key.pem ubuntu@YOUR_ELASTIC_IP
```

---

# 3. Install Docker & Docker Compose

```bash id="p9m1wb"
sudo apt update

sudo apt install docker.io docker-compose-plugin git curl jq awscli -y

sudo systemctl enable docker

sudo systemctl start docker
```

---

# 4. Clone Repository

```bash id="t6x3nv"
git clone <your-github-repo-url>

cd fast-api-task
```

---

# 5. Create AWS Secrets Manager Secret

Go to:

[AWS Secrets Manager Console](https://console.aws.amazon.com/secretsmanager/?utm_source=chatgpt.com)

Create a secret named:

```text id="m2q7zx"
Fast-API-Secrets
```

Secret JSON:

```json id="x8m1kr"
{
  "POSTGRES_DB": "appdb",
  "POSTGRES_USER": "admin",
  "POSTGRES_PASSWORD": "password123",
  "REDIS_HOST": "redis"
}
```

---

# 6. Create IAM Policy

Go to:

[AWS IAM Console](https://console.aws.amazon.com/iam/?utm_source=chatgpt.com)

Create policy:

```json id="f5q9wb"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "*"
    }
  ]
}
```

Policy name example:

```text id="v1m4qx"
FastAPISecretsReadPolicy
```

---

# 7. Create IAM Role

Create IAM Role:

* Trusted Entity:

  * AWS Service
  * EC2

Attach policy:

```text id="q8m2zr"
FastAPISecretsReadPolicy
```

Role name example:

```text id="k3x7nv"
FastAPI-EC2-Secrets-Role
```

---

# 8. Attach IAM Role to EC2

Go to:

```text id="p7m1wb"
EC2
→ Instance
→ Actions
→ Security
→ Modify IAM Role
```

Attach:

```text id="j4q9zx"
FastAPI-EC2-Secrets-Role
```

---

# 9. Verify IAM Access

Run:

```bash id="z6m3kr"
aws sts get-caller-identity
```

Then verify secret access:

```bash id="w2q8nv"
aws secretsmanager get-secret-value \
--secret-id Fast-API-Secrets \
--region us-east-1
```

---

# 10. Make Deployment Script Executable

```bash id="n5m1wb"
chmod +x secrets-loader.sh
```

---

# 11. Start Application

```bash id="x9q4zr"
./secrets-loader.sh
```

---

# 12. Verify Running Containers

```bash id="r3m8vx"
docker compose ps
```

Expected:

```text id="u7q2mk"
fastapi-app   Up
postgres-db   Up (healthy)
redis-cache   Up (healthy)
nginx-proxy   Up
```

---

# 13. Access Application

Open:

```text id="f1m9wb"
http://YOUR_ELASTIC_IP
```

---

# 14. Test APIs

## Health Check

```text id="v4q7zx"
http://YOUR_ELASTIC_IP/health
```

---

# Create User

```bash id="k8m2nv"
curl -X POST http://YOUR_ELASTIC_IP/users \
-H "Content-Type: application/json" \
-d '{"name":"Vaibhav","email":"vaibhav@test.com"}'
```

---

# Get Users

```bash id="m5q1wb"
curl http://YOUR_ELASTIC_IP/users
```

---

# 15. Configure GitHub Actions

Go to:

```text id="p2m8zr"
GitHub Repository
→ Settings
→ Secrets and Variables
→ Actions
```

Add:

| Secret       | Description     |
| ------------ | --------------- |
| EC2_HOST     | Elastic IP      |
| EC2_USERNAME | ubuntu          |
| EC2_SSH_KEY  | Private SSH key |

---

# 16. CI/CD Deployment Flow

Whenever code is pushed to:

```text id="t9q3vx"
main branch
```

GitHub Actions automatically:

1. Connects to EC2
2. Pulls latest code
3. Fetches secrets
4. Rebuilds containers
5. Restarts application

---

# 17. Useful Debugging Commands

## View Logs

```bash id="w6m1qp"
docker logs fastapi-app
```

---

# Live Logs

```bash id="h3q8zr"
docker logs -f fastapi-app
```

---

# Restart Containers

```bash id="c7m2nv"
docker compose restart
```

---

# Stop Containers

```bash id="p1q9wb"
docker compose down
```

---

# Remove Volumes

```bash id="m8x4zr"
docker compose down -v
```

---

# Check Rendered Docker Compose Variables

```bash id="t4m7qx"
docker compose config
```

---

# Verify Container Environment Variables

```bash id="v9q1mk"
docker exec -it fastapi-app env
```


# Author

Vaibhav Shah

DevOps & Backend Engineering Assignment Project
