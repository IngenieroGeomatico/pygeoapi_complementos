# Docu: https://docs.pygeoapi.io/en/latest/plugins.html#example-custom-pygeoapi-vector-data-provider

from pygeoapi.provider.base import BaseProvider, ProviderQueryError

from ..pygdal_PG_datasource.lib.Vector_conex import FuenteDatosVector


class OGR_DataProvider(BaseProvider):
    """Mi proveedorde datos vectoriales OGR"""

    def __init__(self, provider_def):
        """hereda de la clase padre"""
        super().__init__(provider_def)

        self.layer = None
        self.file = provider_def['data']
        self.collection_id = provider_def.get('name', '') 

        # 1. . Si se define en el YAML
        if 'layer' in provider_def:
            self.layer = provider_def['layer']
        # 2. Si no, usar la primera capa disponible
        else:
            fuenteDatos = FuenteDatosVector(self.file)
            fuenteDatos.leer(datasetCompleto=True)
            layers = fuenteDatos.obtener_capas()
            fuenteDatos.datasource =  None

            if not layers:
                raise ProviderQueryError(f"No hay capas disponibles en {self.file}")
            self.layer = layers[0]
            self.layersArray = layers

    def get_fields(self):
        # Aquí se devuelve un objeto con los atributos y su tipo
        return {
            'field1': 'string',
            'field2': 'string'
        }

    def query(self, offset=0, limit=10, resulttype='results',
              bbox=[], datetime_=None, properties=[], sortby=[],
              select_properties=[], skip_geometry=False, **kwargs):
        
        if properties:
            propertiesDict = dict(properties)
            # Se comprueba que exista el valor __Layer__ para sacar la capa que se quiere mostrar
            if '__layer__' in propertiesDict:
                layerValue = propertiesDict['__layer__']

                # Intentar convertir a entero para ver si es numérico en string
                try:
                    int_value = int(layerValue)
                    self.layer = self.layersArray[int_value]
                except (ValueError, TypeError):
                    self.layer = layerValue
                    
        # Se carga el dataset de la capa 
        fuenteDatos = FuenteDatosVector(self.file)
        fuenteDatos.leer(capa=self.layer)
        self.dataset = fuenteDatos
        

        # Se devuelve el resultdo
        gjson = self.dataset.exportar(EPSG_Salida=4326)
        return gjson
    
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