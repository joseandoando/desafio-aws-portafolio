FROM python:3.11-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY local/requirements-local.txt /tmp/requirements-local.txt
RUN pip install --no-cache-dir -r /tmp/requirements-local.txt

CMD ["python", "local/run_local_pipeline.py"]
