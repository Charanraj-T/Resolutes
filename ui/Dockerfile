FROM python:3.11-slim

WORKDIR /app

# Copy app code
COPY . .

# Copy requirements from root
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy service account JSON into container
COPY  gen-lang-client-0351075627-8933c229cee4.json /secrets/key.json

# Set the path inside container
ENV GOOGLE_APPLICATION_CREDENTIALS="/secrets/key.json"

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
