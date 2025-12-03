import os
import csv
from datetime import datetime

DATA_DIR = "data"
LOG_FILE = os.path.join(DATA_DIR, "telemetry_log.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# Ensure CSV header exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "pathway", "latency_ms", "tokens"])


def log_request(pathway: str, latency_ms: int, tokens: int = None):
    """
    Logs telemetry data for each LLM request.
    pathway: RAG / Tool / None
    latency_ms: response time
    tokens: number of tokens used (if available)
    """
    # Works still
    timestamp = datetime.utcnow().isoformat()

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, pathway, latency_ms, tokens])