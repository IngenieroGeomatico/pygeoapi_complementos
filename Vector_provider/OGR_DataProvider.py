# Docu: https://docs.pygeoapi.io/en/latest/plugins.html#example-custom-pygeoapi-vector-data-provider

from pygeoapi.provider.base import BaseProvider, ProviderQueryError

from ..pygdal_PG_datasource.lib.Vector_conex import FuenteDatosVector


class OGR_DataProvider(BaseProvider):
    """Mi proveedorde datos vectoriales OGR"""

    def __init__(self, provider_def):
        """hereda de la clase padre"""
        super().__init__(provider_def)

        self.layer = None
        self.overwriteLinksLayer = False
        self.file = provider_def['data']
        self.collection_id = provider_def.get('name', '') 

        # 1. Si se define en el YAML
        if 'layer' in provider_def:
            self.layer = provider_def['layer']
            self.overwriteLinksLayer = False
            fuenteDatos.leer(capa=self.layer)
            self._fields = fuenteDatos.obtener_atributos(self.layer)
            self.dataset = fuenteDatos
        # 2. Si no, usar la primera capa disponible
        else:
            fuenteDatos = FuenteDatosVector(self.file)
            fuenteDatos.leer(datasetCompleto=True)
            layers = fuenteDatos.obtener_capas()
            atributosPorCapa = fuenteDatos.obtener_atributos()
            self._fields = {}
            for nombre_capa, atributos in atributosPorCapa.items():
                for propiedad, valores in atributos.items():
                    if propiedad not in self._fields:
                        self._fields[propiedad] = valores
            
            if not layers:
                raise ProviderQueryError(f"No hay capas disponibles en {self.file}")
            self.layer = layers[0]
            self.layersArray = layers
            self.overwriteLinksLayer = True
            fuenteDatos.datasource =  None
            self.dataset = None
            

    def get_fields(self):
        self._fields = self.dataset.obtener_atributos(self.layer)
        return self._fields 


    def query(self, offset=0, limit=10, resulttype='results',
              bbox=[], datetime_=None, properties=[], sortby=[],
              select_properties=[], skip_geometry=False, **kwargs):
        
        if properties:
            propertiesDict = dict(properties)
            sqlFilter = None
            # Se comprueba que exista el valor __Layer__ para sacar la capa que se quiere mostrar
            if '__layer__' in propertiesDict:
                layerValue = propertiesDict['__layer__']

                # Intentar convertir a entero para ver si es numérico en string
                try:
                    int_value = int(layerValue)
                    self.layer = self.layersArray[int_value]
                except (ValueError, TypeError):
                    self.layer = layerValue

            # Crear lista de condiciones sin incluir '__layer__'
            condiciones = [f"{k} = '{v}'" for k, v in propertiesDict.items() if k != '__layer__' and k in self._fields]
            # Unir las condiciones con 'AND'
            if condiciones:
                filtro_sql = ' AND '.join(condiciones)
                sqlFilter = True

        self.title = self.layer
                    
        # Se carga el dataset de la capa 
        if not self.dataset:
            fuenteDatos = FuenteDatosVector(self.file)
            fuenteDatos.leer(capa=self.layer)
            self.dataset = fuenteDatos


        if properties and sqlFilter:
            self.dataset.ejecutar_sql(f'select * from "{self.layer}" WHERE {filtro_sql}',
                                    self.layer        
            )  
        
        if bbox:
            self.dataset.MRE_datos(capaEntrada=self.layer, MRE=bbox, EPSG_MRE="EPSG:4326")
        
        if sortby:
            self.dataset.ejecutar_sql(f'select * from "{self.layer}" ORDER BY "{sortby[0]['property']}"',
                                    self.layer,
                                    dialect='SQLITE'            
            )  
            
        if offset:
            self.dataset.ejecutar_sql(f'select * from "{self.layer}" OFFSET {offset}',
                                    self.layer          
            )

        if limit:
            self.dataset.ejecutar_sql(f'select * from "{self.layer}" LIMIT {limit}',
                                    self.layer
            )   
        # viene del parámetro properties
        if select_properties:
            select_str = ', '.join(select_properties)
            self.dataset.ejecutar_sql(f'select {select_str} from "{self.layer}" LIMIT {limit}',
                                    self.layer
            ) 

        # viene del parámetro skipGeometry
        if skip_geometry:
            self.dataset.borrar_geometria(capa=self.layer)
        
        if resulttype == 'hits':
            gjson = {
                'type': 'FeatureCollection',
                'numberMatched': self.dataset.datasource.GetLayerByName(self.layer).GetFeatureCount(),
                'features': []
            }
        else:
            gjson = self.dataset.exportar(EPSG_Salida=4326)

        gjson['name'] = self.layer
        gjson['title'] = f'Capa: {self.layer}'

        if self.overwriteLinksLayer:
            gjson['links'] = [
                {
                    'rel': 'collection',
                    'type': 'application/geo+json',
                    'title': f'Capa: {self.layer} ||',
                    'href': f'/collections/OGR_1/items?__layer__={self.layer}'
                }
        ]
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