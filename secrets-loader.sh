#!/bin/bash

echo "Fetching secrets from AWS Secrets Manager..."

SECRET_JSON=$(aws secretsmanager get-secret-value \
  --secret-id Fast-API-Secrets \
  --region us-east-2 \
  --query SecretString \
  --output text)

if [ $? -ne 0 ]; then
  echo "Failed to fetch secrets!"
  exit 1
fi

export POSTGRES_DB=$(echo $SECRET_JSON | jq -r .POSTGRES_DB)
export POSTGRES_USER=$(echo $SECRET_JSON | jq -r .POSTGRES_USER)
export POSTGRES_PASSWORD=$(echo $SECRET_JSON | jq -r .POSTGRES_PASSWORD)
export REDIS_HOST=$(echo $SECRET_JSON | jq -r .REDIS_HOST)

echo "Secrets loaded successfully."

docker compose down

docker compose up -d --build