#!/bin/bash
set -e

# -----------------------------
# Variables
# -----------------------------
PROJECT_ID="gen-lang-client-0351075627"
IMAGE_NAME="streamlit-ui"
IMAGE_TAG="latest"
REGION="us-central1"
REPO_NAME="streamlit-repo"
GAR_IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:$IMAGE_TAG"
SERVICE_NAME="streamlit-ui-service"
SECRET_FILE="/Users/kavinkumarbaskar/project/deep-research-agents/gen-lang-client-0351075627-8933c229cee4.json"
ENV_FILE=".env"

AGENT_FOLDER="adk"
AGENT_DISPLAY_NAME="deep-research-agents"

# -----------------------------
# Check .env file
# -----------------------------
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found!"
    exit 1
fi

# Convert .env to comma-separated list for Cloud Run
ENV_VARS=$(grep -v '^#' "$ENV_FILE" | xargs | sed 's/ /,/g')

# Extract specific env variables for ADK (e.g., MONGO_URI)
MONGO_URI=$(grep -v '^#' "$ENV_FILE" | grep 'MONGO_URI' | cut -d '=' -f2-)

# -----------------------------
# Authenticate with GCP
# -----------------------------
if [ ! -f "$SECRET_FILE" ]; then
    echo "Error: $SECRET_FILE not found!"
    exit 1
fi

echo "Authenticating with Google Cloud..."
gcloud auth activate-service-account --key-file="$SECRET_FILE"
gcloud config set project "$PROJECT_ID"

# -----------------------------
# Deploy to Cloud Run
# -----------------------------
echo "Deploying to Cloud Run..."
gcloud run deploy "$SERVICE_NAME" \
    --image "$GAR_IMAGE" \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --port 8501 \
    --set-env-vars "$ENV_VARS" \
    --min-instances 1

# Get deployed service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" \
    --platform managed \
    --region "$REGION" \
    --format "value(status.url)")

echo "✅ Cloud Run deployment complete!"
echo "Your Cloud Run service URL: $SERVICE_URL"

# -----------------------------
# Deploy ADK Remote Agent
# -----------------------------
# echo "Deploying Remote Agent..."
# python -m deployment.deploy --create \
#     --agent_folder="$AGENT_FOLDER" \
#     --display_name="$AGENT_DISPLAY_NAME" \
#     --custom_env="MONGO_URI=$MONGO_URI"

# echo "✅ Remote Agent deployed!"
