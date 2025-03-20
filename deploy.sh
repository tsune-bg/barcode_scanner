#!/bin/bash
set -e

# .env ファイルから変数を読み込む
if [ -f .env ]; then
  # .env がシェル形式になっている場合は "source" でもOK
  # ここではコメント行を除去してエクスポートしています
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found"
  exit 1
fi

IMAGE_URI="${LOCATION}-docker.pkg.dev/${PROJECT}/${REPOSITORY}/${IMAGE_NAME}:${TAG}"

echo "=== Building and pushing image with Cloud Build ==="
echo "Image URI: ${IMAGE_URI}"
gcloud builds submit --tag ${IMAGE_URI}

echo "=== Deploying to Cloud Run ==="
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_URI} \
  --platform managed \
  --region ${LOCATION} \
  --allow-unauthenticated \
  --update-secrets=${ENV_VAR_NAME}=${SECRET_NAME}:latest

echo "Deployment completed!"
