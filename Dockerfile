FROM python:3.13-slim-bookworm

WORKDIR /app


# Install system deps
RUN apt-get update -y && apt-get install -y --no-install-recommends libpq-dev gcc postgresql-client && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt entrypoint.sh ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && chmod +x entrypoint.sh

COPY . .

ENTRYPOINT ["sh","entrypoint.sh"]
