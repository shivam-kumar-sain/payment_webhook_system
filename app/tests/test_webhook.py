import json
import subprocess
from datetime import datetime
from pathlib import Path


"""
    --------------------------------------------------
    Paths
    --------------------------------------------------
"""

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "webhook_test_logs.json"


"""
    --------------------------------------------------
    CURL Command
    --------------------------------------------------
"""

command = [
    "curl",
    "-X",
    "POST",
    "http://127.0.0.1:8000/webhook/payments",
    "-H",
    "Content-Type: application/json",
    "-H",
    "X-Razorpay-Signature: test_secret",
    "-d",
    "@mock_payloads/payment_authorized.json"
]


"""
    --------------------------------------------------
    Execute CURL
    --------------------------------------------------
"""

result = subprocess.run(
    command,
    capture_output=True,
    text=True
)


"""
    --------------------------------------------------
    Create Log Data
    --------------------------------------------------
"""

log_data = {
    "timestamp": datetime.utcnow().isoformat(),
    "command": " ".join(command),
    "status_code": result.returncode,
    "stdout": result.stdout,
    "stderr": result.stderr,
}


"""
    --------------------------------------------------
    Convert Response To JSON If Possible
    --------------------------------------------------
"""

try:
    parsed_response = json.loads(result.stdout)
    log_data["response_json"] = parsed_response
except Exception:
    log_data["response_json"] = None


"""
    --------------------------------------------------
    Save Logs
    --------------------------------------------------
"""

existing_logs = []
if LOG_FILE.exists():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            existing_logs = json.load(file)
    except Exception:
        existing_logs = []

existing_logs.append(log_data)
with open(LOG_FILE, "w", encoding="utf-8") as file:
    json.dump(
        existing_logs,
        file,
        indent=4,
        ensure_ascii=False
    )


"""
    --------------------------------------------------
    Print Result
    --------------------------------------------------
"""

print("\nWebhook Test Completed")
print(f"\nLog File Saved At:\n{LOG_FILE}")
print("\nResponse:\n")
try:
    print(
        json.dumps(
            parsed_response,
            indent=4
        )
    )

except Exception:
    print(result.stdout)