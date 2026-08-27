import os
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

datos = respuesta.json()

print(datos)
