
# Evaluacion2

## Descripción del proyecto

Este proyecto corresponde a la evaluación CUY6142. Incluye un programa desarrollado en Python que utiliza GraphHopper Directions API para calcular rutas entre coordenadas geográficas.

## Funcionalidades

- Solicitud de coordenadas de origen y destino.
- Consulta de rutas mediante GraphHopper.
- Visualización de distancias y tiempos con un máximo de dos decimales.
- Presentación de instrucciones de viaje en español.
- Opción de salir escribiendo `s` o `salir`.
- Manejo de errores de conexión y respuestas HTTP.

## Requisitos

- Python 3.
- Biblioteca `requests`.
- Clave API válida de GraphHopper.
- Conexión a Internet.

## Instalación

Instalar la dependencia:

```bash
python3 -m pip install requests
```

## Configuración de la clave API

Definir la variable de entorno con tu propia clave:

```bash
export GRAPHHOPPER_API_KEY='TU_CLAVE_API'
```

No publiques tu clave API ni la incluyas en el repositorio.

## Ejecución

Desde la carpeta del proyecto, ejecutar:

```bash
python3 geolocalizacion.py
```

Introduce las coordenadas que solicite el programa. Para salir, escribe `s` o `salir`.

## Archivos

- `geolocalizacion.py`: programa de geolocalización.
- `README.md`: descripción e instrucciones de uso.

## Autor

Nombre del estudiante: completar.

## Repositorio GitHub

Enlace: completar después de publicar el repositorio.
