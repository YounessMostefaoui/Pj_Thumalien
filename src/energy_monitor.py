# Exemple simple avec influxdb-client en Python
from influxdb_client import InfluxDBClient

def read_energy_metrics():
    client = InfluxDBClient(url="http://localhost:8086", token="VOTRE_TOKEN", org="votre_org")
    query_api = client.query_api()
    result = query_api.query('from(bucket:"energy") |> range(start: -5m) |> filter(fn: (r) => r._measurement == "cpu")')
    return result

'''Récupère les données système en temps réel depuis InfluxDB.

Permet de suivre la consommation CPU, RAM ou autre.'''