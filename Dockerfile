# Stage 1: Build stage
FROM python:3.13-slim-bookworm AS builder
WORKDIR /app

# Install build deps (removed in final image)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential libpq-dev gcc \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Stage 2: Final runtime
FROM python:3.13-slim-bookworm
WORKDIR /app

# Install only runtime deps
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    libpq5 postgresql-client \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy entrypoint and source
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
COPY . .

ENTRYPOINT ["sh", "entrypoint.sh"]
