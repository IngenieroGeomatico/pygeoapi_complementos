# random_number_process.py

import logging
from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError

from ..pygdal_PG_datasource.lib.Vector_conex import FuenteDatosVector
from ..pygdal_PG_datasource.procesos.vector.geoprocesos import crear_capa_buffer_OGR

LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.3.0',
    'id': 'buffer_data',
    'title': {
        'en': 'Buffer Area Process',
        'es': 'Proceso de Área de Influencia (Buffer)'
    },
    'description': {
        'en': 'Generates a buffer area around geometries from an input vector layer.',
        'es': 'Genera un área de influencia (buffer) alrededor de las geometrías de una capa vectorial de entrada.'
    },
    'jobControlOptions': ['sync-execute', 'async-execute'],
    'keywords': ['buffer', 'area', 'influence', 'vector', 'geoprocessing'],
    'links': [{
        'type': 'text/html',
        'rel': 'about',
        'title': 'buffer process info',
        'href': 'https://example.org/process/buffer',
        'hreflang': 'en-US'
    }],
    'inputs': {
        'data': {
            'title': 'Data source',
            'description': 'Ruta o URL del datasource vectorial de entrada',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'keywords': ['datasource', 'vector']
        },
        'capa': {
            'title': 'Layer name',
            'description': 'Nombre de la capa dentro del datasource a procesar',
            'schema': {
                'type': 'string'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'keywords': ['layer', 'vector']
        },
        'EPSG_entrada': {
            'title': 'EPSG código de entrada',
            'description': 'Código EPSG del sistema de referencia de entrada (por defecto 4326)',
            'schema': {
                'type': 'integer'
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'default': 4326,
            'keywords': ['crs', 'epsg', 'entrada']
        },
        'EPSG_salida': {
            'title': 'EPSG código de salida',
            'description': 'Código EPSG del sistema de referencia de salida (por defecto 4326)',
            'schema': {
                'type': 'integer'
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'default': 4326,
            'keywords': ['crs', 'epsg', 'salida']
        },
        'distancia_buffer': {
            'title': 'Distancia de buffer',
            'description': 'Distancia (en unidades del CRS) para crear el buffer',
            'schema': {
                'type': 'number'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'default': 1000,
            'keywords': ['buffer', 'distancia', 'area']
        },
        'outputFormat': {
            'title': 'Formato de salida',
            'description': 'Formato del resultado (por defecto json)',
            'schema': {
                'type': 'string',
                'enum': ['json', 'geojson', 'gml', 'xml']
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'default': 'json',
            'keywords': ['format', 'output']
        }
    },
    'outputs': {
        'result': {
            'title': 'Resultado',
            'description': 'Resultado con la capa buffer generada',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'data': "POINT (-3 40)",
            'capa': 0,
            'EPSG_entrada': 4326,
            'EPSG_salida': 4326,
            'outputFormat': 'json',
            'distancia_buffer': 1000
        }
    }
}


class bufferDataProcessor(BaseProcessor):
    """Devuelve el área de influencia a partir de unos datos"""

    def __init__(self, provider_def):
        super().__init__(provider_def, PROCESS_METADATA)
        self.supports_outputs = True
        self.name = "buffer_data"

    def execute(self, data: dict, outputs: dict = None) -> dict:

        try:
            datasource = data.get('data', None)
            capa = data.get('capa', None)
            EPSG_entrada = data.get('EPSG_entrada', 4326)
            EPSG_salida = data.get('EPSG_salida', 4326)
            outputFormat = data.get('outputFormat', 'json')

            fuenteDatos =  FuenteDatosVector(datasource)
            fuenteDatos.leer(capa=capa, EPSG_Entrada=EPSG_entrada)
            fuenteDatos.reproyectar_datasource(EPSG_salida=3857)

            ds_buffer, capaBuffer = crear_capa_buffer_OGR(
                layer=fuenteDatos.datasource.GetLayerByIndex(0),
                distancia_buffer=data.get('distancia_buffer', 1000),
                nombre_capa_salida=fuenteDatos.datasource.GetLayerByIndex(0).GetName()
            )

            fuenteDatos.añadir_capa(capaBuffer)
            fuenteDatos.reproyectar_datasource(EPSG_salida=EPSG_salida)
            outData = fuenteDatos.exportar(EPSG_Salida=EPSG_salida, outputFormat=outputFormat)

            outputs = {
                'result': outData,
                'outputFormat': outputFormat,
            }
            
            mimetype = 'application/json'
            return mimetype, outputs
             
        except Exception as err:
            raise ProcessorExecuteError(f'Error ejecutando el proceso: {err}')

    def __repr__(self):
        return f'<BufferDataProcessor> {self.name}'

