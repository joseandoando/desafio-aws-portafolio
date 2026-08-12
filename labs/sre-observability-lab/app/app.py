import os
import random
import time

from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUESTS = Counter(
    "demo_http_requests_total",
    "Total HTTP requests",
    ["path", "status"],
)
LATENCY = Histogram(
    "demo_http_request_duration_seconds",
    "HTTP request latency",
    ["path"],
)

START_TIME = time.time()


def record(path: str, status: int, started: float):
    REQUESTS.labels(path=path, status=str(status)).inc()
    LATENCY.labels(path=path).observe(time.time() - started)


@app.get("/")
def index():
    started = time.time()
    delay_ms = int(os.getenv("APP_DELAY_MS", "25"))
    time.sleep(delay_ms / 1000)
    record("/", 200, started)
    return jsonify(
        service="sre-observability-lab",
        status="ok",
        uptime_seconds=round(time.time() - START_TIME, 2),
    )


@app.get("/health")
def health():
    started = time.time()
    record("/health", 200, started)
    return jsonify(status="healthy"), 200


@app.get("/ready")
def ready():
    started = time.time()
    record("/ready", 200, started)
    return jsonify(status="ready"), 200


@app.get("/simulate/error")
def simulate_error():
    started = time.time()
    record("/simulate/error", 500, started)
    return jsonify(error="simulated production failure for alert testing"), 500


@app.get("/simulate/latency")
def simulate_latency():
    started = time.time()
    time.sleep(random.uniform(0.6, 1.2))
    record("/simulate/latency", 200, started)
    return jsonify(status="slow request completed"), 200


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
