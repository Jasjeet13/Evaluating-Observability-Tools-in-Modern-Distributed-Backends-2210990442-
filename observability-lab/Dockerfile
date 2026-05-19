# Build: docker build --build-arg SERVICE=gateway -t observability-lab/gateway .
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY lab ./lab
COPY services ./services

ARG SERVICE=gateway
ENV SERVICE=${SERVICE}

EXPOSE 8080
CMD ["sh", "-c", "python -m services.${SERVICE}.main"]
