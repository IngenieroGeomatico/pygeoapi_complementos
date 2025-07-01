# Docu: https://docs.pygeoapi.io/en/latest/plugins.html#example-custom-pygeoapi-vector-data-provider

from pygeoapi.provider.base import BaseProvider, ProviderQueryError

from ..pygdal_PG_datasource.lib.Vector_conex import FuenteDatosVector
# from pygeoapi.pygeoapi_complementos.pygdal_PG_datasource.lib.Vector_conex import FuenteDatosVector

import json

class OGR_DataProvider(BaseProvider):
    """Mi proveedorde datos vectoriales OGR"""

    def __init__(self, provider_def):
        """hereda de la clase padre"""
        super().__init__(provider_def)

        self.file = provider_def['data']
        self.collection_id = provider_def.get('name', '') 
        self.layer = None

        # 1. Si tiene "__", usar parte final como nombre de capa
        if '__layer__' in self.collection_id:
            self.layer = self.collection_id.split('__layer__', 1)[1]
        # 2. Si se define en el YAML
        elif 'layer' in provider_def:
            self.layer = provider_def['layer']
        # 3. Si no, usar la primera capa disponible
        else:
            fuenteDatos = FuenteDatosVector(self.file)
            dataset = fuenteDatos.leer()
            layers = fuenteDatos.obtener_capas()

            if not layers:
                raise ProviderQueryError(f"No hay capas disponibles en {self.file}")
            self.layer = layers[0]

        # Abre la capa
        self.dataset = fuenteDatos

    def get_fields(self):
        # Aquí se devuelve un objeto con los atributos y su tipo
        return {
            'field1': 'string',
            'field2': 'string'
        }

    def query(self, offset=0, limit=10, resulttype='results',
              bbox=[], datetime_=None, properties=[], sortby=[],
              select_properties=[], skip_geometry=False, **kwargs):

        # Se puede especificar opcionalmente el nombre del archivo de salida
        self.filename = 'ogr.dat'

        # Se devuelve el resultdo
        gjson = self.dataset.exportar(EPSG_Salida=4326)
        print(gjson)
        return json.loads(gjson)
    
    def get(self, identifier):
        # Devuelve un solo objeto por ID
        return {
            'type': 'Feature',
            'id': identifier,
            'geometry': {
                'type': 'Point',
                'coordinates': [1.0, 1.0]
            },
            'properties': {
                'id': identifier,
                'nombre': 'Punto único'
            }
        }

    def get_schema():
        # return a `dict` of a JSON schema (inline or reference)
        return ('application/geo+json', {'$ref': 'https://geojson.org/schema/Feature.json'})