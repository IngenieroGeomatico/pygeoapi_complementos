# Docu: https://docs.pygeoapi.io/en/latest/plugins.html#example-custom-pygeoapi-vector-data-provider

from pygeoapi.provider.base import BaseProvider, ProviderQueryError

class OGVectorDataProvider(BaseProvider):
    """My cool vector data provider"""

    def __init__(self, provider_def):
        """Inherit from parent class"""

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
            layers = None  # Usar aquí una función para obtener las capas

            if not layers:
                raise ProviderQueryError(f"No hay capas disponibles en {self.file}")
            self.layer = layers[0]

        # Abre la capa
        self.dataset = None # Usar aquí una función para devolver el dataset

    def get_fields(self):

        # open dat file and return fields and their datatypes
        return {
            'field1': 'string',
            'field2': 'string'
        }

    def query(self, offset=0, limit=10, resulttype='results',
              bbox=[], datetime_=None, properties=[], sortby=[],
              select_properties=[], skip_geometry=False, **kwargs):

        # optionally specify the output filename pygeoapi can use as part
        # of the response (HTTP Content-Disposition header)
        self.filename = 'my-cool-filename.dat'

        # open data file (self.data) and process, return
        return {
            'type': 'FeatureCollection',
            'features': [{
                'type': 'Feature',
                'id': '371',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [ -75, 45 ]
                },
                'properties': {
                    'stn_id': '35',
                    'datetime': '2001-10-30T14:24:55Z',
                    'value': '89.9'
                }
            }]
        }
    
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