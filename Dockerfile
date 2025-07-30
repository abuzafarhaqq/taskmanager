FROM python:3.13-slim

WORKDIR /app

# Install system deps + PostgreSQL client  

RUN apt-get update
RUN apt-get install -y --no-install-recommends libpq-dev gcc curl postgresql-client && rm -rf /var/lib/apt/lists/*


# Install python dependecies
COPY requirements.txt entrypoint.sh ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt \
&& chmod +x entrypoint.sh
COPY . .

# CMD ["flask","run"]

ENTRYPOINT ["sh","entrypoint.sh"]
