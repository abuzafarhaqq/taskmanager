FROM python:3.11-slim

WORKDIR /app

# Install system deps + PostgreSQL client  
RUN apt update && apt upgrade -y
RUN apt install -y --no-install-recommends gcc libpq-dev postgresql-client
RUN rm -rf /var/lib/apt/lists/*  
# RUN echo {$pwd} && ls -lR

COPY requirements.txt entrypoint.sh ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt \
&& chmod +x entrypoint.sh
COPY . .

# CMD ["flask","run"]

ENTRYPOINT ["sh","entrypoint.sh"]
