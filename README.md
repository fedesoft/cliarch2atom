# Proyecto migración de CliArch a AtoM

## Descripción General

Este proyecto es una solución integral para la migración de CliArch a AtoM (Access to Memory), enfocándose específicamente en las descripciones archivísticas siguiendo las normas ISAD(G). La funcionalidad principal gira en torno al script `clasificacion_isad.py`, que interactúa con múltiples módulos de soporte para extraer, transformar y cargar descripciones archivísticas en AtoM.

## Estructura del Proyecto

- `clasificacion_isad.py`: Script principal que genera los CSVs de importación hacía AtoM.
- `helpers.py`: Módulo con funciones auxiliares.
- `raw_queries.py`: Contiene las consultas SQL utilizadas para extraer los datos de SQL Server.
- `test_signatures.py`: Pruebas para validar el formato y generación de firmas.
- `ingreso.py`, `estado_fisico.py`, `atom_description_headers.py`: Módulos que definen datos constantes como el origen de ingreso, estado físico de los documentos y cabeceras de descripción para AtoM.
- `src.py`: Script adicional que proporciona funcionalidades relacionadas pero distintas a las de `clasificacion_isad.py`.
- `notes.md`: Notas sobre el proceso de migración y comandos útiles.
- `niveldescripcion_2023.csv`: Base de los niveles de descripción.

## Requisitos

- Python 3.8+
- pymssql para la conexión con SQL Server.
- anytree para la construcción de la estructura jerárquica de las descripciones archivísticas.
- Otras dependencias especificadas en `requirements.txt` (crear este archivo si es necesario).

## Instalación

1. Clone el repositorio en su máquina local.
2. Instale las dependencias necesarias usando `pip install -r requirements.txt`.
3. Asegúrese de tener acceso a una instancia de SQL Server.

## Uso

Para ejecutar la migración, use el siguiente comando:

```bash
python clasificacion_isad.py [ARGUMENTO]
```

Donde `[ARGUMENTO]` es uno de los códigos de clasificación que desea procesar (por ejemplo, `A1`, `F1`, `S1`, `M1`).
