
#!/usr/bin/env python3

import os
import requests

API_URL = "https://graphhopper.com/api/1/route"


def formato_numero(valor):
    """Muestra números con un máximo de dos decimales."""
    return f"{valor:.2f}".rstrip("0").rstrip(".")


def pedir_coordenada(mensaje, minimo, maximo):
    """Solicita una coordenada y permite salir con s o salir."""
    while True:
        entrada = input(mensaje).strip()

        if entrada.lower() in ("s", "salir"):
            return None

        try:
            valor = float(entrada.replace(",", "."))

            if minimo <= valor <= maximo:
                return valor

            print(f"Error: introduce un valor entre {minimo} y {maximo}.")
        except ValueError:
            print("Entrada no válida. Escribe un número, 's' o 'salir'.")


def consultar_ruta(lat_origen, lon_origen, lat_destino, lon_destino, clave):
    parametros = {
        "point": [
            f"{lat_origen},{lon_origen}",
            f"{lat_destino},{lon_destino}"
        ],
        "profile": "car",
        "locale": "es",
        "key": clave,
        "instructions": "true",
        "calc_points": "true"
    }

    respuesta = requests.get(API_URL, params=parametros, timeout=30)
    respuesta.raise_for_status()

    datos = respuesta.json()

    if not datos.get("paths"):
        raise ValueError("La API no devolvió ninguna ruta.")

    return datos["paths"][0]


def ejecutar():
    clave = os.getenv("GRAPHHOPPER_API_KEY")

    if not clave:
        print(
            "Error: no se encontró la clave API de GraphHopper.\n"
            "Configura la variable GRAPHHOPPER_API_KEY antes de ejecutar."
        )
        return

    print("=" * 55)
    print("       SISTEMA DE GEOLOCALIZACIÓN")
    print("=" * 55)
    print("Introduce las coordenadas geográficas.")
    print("Escribe 's' o 'salir' en cualquier momento para terminar.\n")

    while True:
        lat_origen = pedir_coordenada(
            "Latitud de origen (-90 a 90): ", -90, 90
        )
        if lat_origen is None:
            break

        lon_origen = pedir_coordenada(
            "Longitud de origen (-180 a 180): ", -180, 180
        )
        if lon_origen is None:
            break

        lat_destino = pedir_coordenada(
            "Latitud de destino (-90 a 90): ", -90, 90
        )
        if lat_destino is None:
            break

        lon_destino = pedir_coordenada(
            "Longitud de destino (-180 a 180): ", -180, 180
        )
        if lon_destino is None:
            break

        try:
            print("\nConsultando la ruta...")
            ruta = consultar_ruta(
                lat_origen, lon_origen,
                lat_destino, lon_destino,
                clave
            )

            distancia_km = ruta["distance"] / 1000
            tiempo_minutos = ruta["time"] / 60000

            print("\n--- RESULTADO DE LA RUTA ---")
            print(f"Distancia total: {formato_numero(distancia_km)} km")
            print(
                f"Tiempo estimado: "
                f"{formato_numero(tiempo_minutos)} minutos"
            )

            instrucciones = ruta.get("instructions", [])

            print("\n--- NARRATIVA DEL VIAJE ---")

            if not instrucciones:
                print("La API no devolvió instrucciones para esta ruta.")
            else:
                for numero, instruccion in enumerate(instrucciones, start=1):
                    texto = instruccion.get(
                        "text", "Continúa por la ruta indicada."
                    )
                    distancia = instruccion.get("distance", 0) / 1000
                    tiempo = instruccion.get("time", 0) / 60000

                    print(f"{numero}. {texto}")
                    print(
                        f"   Distancia: {formato_numero(distancia)} km"
                        f" | Tiempo: {formato_numero(tiempo)} minutos"
                    )

        except requests.exceptions.HTTPError as error:
            print(f"Error HTTP al consultar la ruta: {error}")
            if error.response is not None:
                print("Detalle del servidor:", error.response.text[:300])
        except requests.exceptions.RequestException as error:
            print(f"Error de conexión con GraphHopper: {error}")
        except (ValueError, KeyError, TypeError) as error:
            print(f"No se pudo procesar la respuesta: {error}")

        print()

    print("Programa finalizado. ¡Hasta pronto!")


if __name__ == "__main__":
    try:
        ejecutar()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma finalizado.")