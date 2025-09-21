#!/bin/bash
set -e

# Variables
PROJECT_ID="gen-lang-client-0351075627"
IMAGE_NAME="streamlit-ui"
IMAGE_TAG="latest"
REGION="us-central1"                    # Artifact Registry location
REPO_NAME="streamlit-repo"              # Artifact Registry repository
GAR_IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:$IMAGE_TAG"
UI_DIR="ui"
SECRET_FILE="/Users/kavinkumarbaskar/project/deep-research-agents/gen-lang-client-0351075627-8933c229cee4.json"

# Authenticate with GCP
if [ ! -f "$SECRET_FILE" ]; then
    echo "Error: $SECRET_FILE not found!"
    exit 1
fi

echo "Authenticating with Google Cloud..."
gcloud auth activate-service-account --key-file="$SECRET_FILE"
gcloud config set project "$PROJECT_ID"

# Configure Docker for Artifact Registry
echo "Configuring Docker to use Artifact Registry..."
gcloud auth configure-docker "$REGION-docker.pkg.dev"

# Check if repository exists; create if it doesn't
if ! gcloud artifacts repositories describe "$REPO_NAME" --location "$REGION" &>/dev/null; then
    echo "Repository $REPO_NAME does not exist. Creating it..."
    gcloud artifacts repositories create "$REPO_NAME" \
        --repository-format=docker \
        --location "$REGION" \
        --description="Docker repo for Streamlit app"
else
    echo "Repository $REPO_NAME already exists."
fi

# Build Docker image
echo "Building Docker image..."
docker build -t "$IMAGE_NAME" "$UI_DIR" --platform linux/amd64

# Tag and push to Artifact Registry
echo "Tagging image as $GAR_IMAGE..."
docker tag "$IMAGE_NAME" "$GAR_IMAGE"

echo "Pushing image to Artifact Registry..."
docker push "$GAR_IMAGE"

echo "✅ Docker image pushed: $GAR_IMAGE"
