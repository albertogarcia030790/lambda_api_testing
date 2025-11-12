# lambda_api/app.py
import json
import time
import os

# Simula trabajo variable (latencia), configurable por query param
def handler(event, context):
    # ejemplo de lectura de body o query params
    method = event.get("httpMethod") if "httpMethod" in event else event.get("requestContext", {}).get("http", {}).get("method","GET")
    # lee delay en ms desde querystring (opcional)
    qparams = event.get("queryStringParameters") or {}
    delay_ms = int(qparams.get("delay_ms", "0"))
    if delay_ms > 0:
        time.sleep(delay_ms / 1000.0)

    resp = {
        "status": "ok",
        "method": method,
        "message": "Hello from Lambda",
        "env": {
            "memory_limit_in_mb": os.environ.get("AWS_LAMBDA_FUNCTION_MEMORY_SIZE")
        }
    }
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(resp)
    }
