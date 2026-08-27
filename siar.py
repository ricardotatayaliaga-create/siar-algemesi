import os
import csv
import requests
from datetime import date, timedelta

TOKEN = os.environ["SIAR_TOKEN"]

BASE_URL = "https://servicio.mapa.gob.es/siarapi/API/V1/Datos/Diarios/ESTACION"

ayer = date.today() - timedelta(days=1)
fecha = ayer.strftime("%Y-%m-%d")

params = {
    "token": TOKEN,
    "Id": "V14",
    "FechaInicial": fecha,
    "FechaFinal": fecha,
    "DatosCalculados": "true",
}

respuesta = requests.get(BASE_URL, params=params, timeout=30)
respuesta.raise_for_status()

resultado = respuesta.json()

datos = resultado.get("datos", [])

if not datos:
    print(f"No hay datos disponibles para {fecha}")
else:
    dato = datos[0]

    fila = {
        "Fecha": dato.get("Fecha"),
        "Estacion": dato.get("Estacion"),
        "TempMedia": dato.get("TempMedia"),
        "TempMax": dato.get("TempMax"),
        "TempMin": dato.get("TempMin"),
        "HumedadMedia": dato.get("HumedadMedia"),
        "Precipitacion": dato.get("Precipitacion"),
        "PrecipitacionEfectiva": dato.get("PePMon"),
        "ETo": dato.get("EtPMon"),
    }

    archivo = "datos_algemesi.csv"

    existe = os.path.exists(archivo)

    with open(archivo, "a", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=fila.keys())

        if not existe:
            escritor.writeheader()

        escritor.writerow(fila)

    print("Dato guardado correctamente:")
    print(fila)
