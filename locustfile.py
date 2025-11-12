from locust import HttpUser, task, between, events
import csv
import time
import os

# === CONFIGURACIÓN ===
RESULTS_FILE = "locust_results.csv"
API_PATH = "/test"  # Cambia este endpoint si tu Lambda usa otro path

# === CLASE PRINCIPAL ===
class LambdaApiUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://YOUR_API_GATEWAY_URL.execute-api.us-east-1.amazonaws.com/prod"

    @task(3)
    def get_request(self):
        """Simula una solicitud GET exitosa"""
        with self.client.get(API_PATH, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error GET {response.status_code}")

    @task(1)
    def post_request(self):
        """Simula una solicitud POST con datos JSON"""
        payload = {"test": "data", "timestamp": time.time()}
        with self.client.post(API_PATH, json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Error POST {response.status_code}")

    @task(1)
    def get_not_found(self):
        """Simula solicitudes a un endpoint inexistente (para probar errores 404)"""
        with self.client.get("/invalid-endpoint", catch_response=True) as response:
            if response.status_code == 404:
                response.success()
            else:
                response.failure(f"Esperado 404, recibido {response.status_code}")


# === CAPTURA DE RESULTADOS Y EXPORTACIÓN A CSV ===
@events.request.add_listener
def log_request(request_type, name, response_time, response_length, response, **kwargs):
    """Captura todas las solicitudes y las escribe en un CSV"""
    file_exists = os.path.isfile(RESULTS_FILE)

    with open(RESULTS_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["timestamp", "method", "endpoint", "response_time_ms", "status_code", "success"])
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            request_type,
            name,
            response_time,
            response.status_code if response else "N/A",
            "true" if response and response.ok else "false"
        ])
