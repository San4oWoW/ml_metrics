import os
import time
import random

from prometheus_client import Histogram, start_http_server

LATENCY = Histogram(
    "request_latency_seconds",
    "Request latency in seconds"
)

SLOW_MODE = os.getenv("SLOW_MODE", "0") == "1"


def handle_request():
    start_time = time.time()

    if SLOW_MODE:
        time.sleep(2.0)
    else:
        simulated_latency = random.uniform(0.05, 0.3)
        time.sleep(simulated_latency)

    elapsed = time.time() - start_time
    LATENCY.observe(elapsed)


def main():
    start_http_server(8000)
    print("Metrics server is running on http://localhost:8000/metrics")
    print(f"SLOW_MODE = {SLOW_MODE}")

    while True:
        handle_request()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
