import pandas as pd
import matplotlib.pyplot as plt
import os

# Ruta base donde guardaste los archivos CSV de JMeter
base_path = "/Volumes/Externo/lambda_api"

# Archivos de resultados (ajusta los nombres si cambian)
files = {
    "100 users": os.path.join(base_path, "results_100users.csv"),
    "500 users": os.path.join(base_path, "results_500users.csv"),
    "1000 users": os.path.join(base_path, "results_1000users.csv"),
}

# Diccionarios para almacenar resultados
avg_response = {}
avg_latency = {}
success_rate = {}

# Procesar cada archivo
for label, file in files.items():
    df = pd.read_csv(file)

    # Calcular métricas
    avg_response[label] = df["elapsed"].mean()
    avg_latency[label] = df["Latency"].mean()
    success_rate[label] = (df["success"].astype(str).str.lower() == "true").mean() * 100

# Crear DataFrame resumen
results = pd.DataFrame({
    "Concurrent Users": list(files.keys()),
    "Avg Response Time (ms)": list(avg_response.values()),
    "Avg Latency (ms)": list(avg_latency.values()),
    "Success Rate (%)": list(success_rate.values())
})

print("\n=== AWS Lambda API Performance (JMeter Results) ===\n")
print(results.to_string(index=False))

# Gráfica 1: Tiempos de respuesta y latencia
plt.figure(figsize=(8, 5))
plt.plot(results["Concurrent Users"], results["Avg Response Time (ms)"], marker='o', label='Response Time')
plt.plot(results["Concurrent Users"], results["Avg Latency (ms)"], marker='s', label='Latency')
plt.title("AWS Lambda API Performance - Response Time vs Latency")
plt.xlabel("Concurrent Users")
plt.ylabel("Milliseconds (ms)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Gráfica 2: Tasa de éxito
plt.figure(figsize=(8, 4))
plt.bar(results["Concurrent Users"], results["Success Rate (%)"], color='green', alpha=0.7)
plt.title("AWS Lambda API - Success Rate")
plt.xlabel("Concurrent Users")
plt.ylabel("Success Rate (%)")
plt.ylim(0, 105)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
