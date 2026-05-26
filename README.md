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

# Author

Vaibhav Shah

DevOps & Backend Engineering Assignment Project
