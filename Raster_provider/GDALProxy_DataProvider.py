from pygeoapi.provider.base import BaseProvider, ProviderQueryError, ProviderConnectionError

from ..pygdal_PG_datasource.lib.Raster_conex import FuenteDatosRaster

class GDALProxyRasterProvider(BaseProvider):
    """Mi proveedorde datos Ráster GDAL"""

    def __init__(self, provider_def):
        """Hereda de la clase padre"""
        super().__init__(provider_def)

        format= {
                "name": '',
                "longName": '',
                "mimetype": ""
        }
        provider_def['format'] = format

        self.__url__ = '__url__'
        self.__properties__ = '__properties__'
        self._coverage_properties = {
            'axes': {},
            'bbox_crs': 4326,
            'num_bands': 0,
            'width': 0,
            'height': 0,
            'resx': 0.0,
            'resy': 0.0
        }
        self._fields = {}
        self.dataset = None
        
    def __repr__(self):
        return f'<GDALPROXYProvider>'

    def get_fields(self):
        """
        Devuelve los metadatos del ráster (equivalente a schema de vectores).
        """
        self._fields = self.dataset.obtener_atributos()
        return self._fields

    def query(self, properties=[], subsets={}, bbox=None, bbox_crs=4326,
              datetime_=None, format_='json', **kwargs):
        """
        Método principal para consultas.
        Por ahora: devuelve info básica del ráster y opcionalmente datos completos.
        """

        if self.__url__  in kwargs:
            self.file = kwargs[self.__url__]
            fuenteDatos = FuenteDatosRaster(self.file)
            fuenteDatos.leer(datasetCompleto=True)
            self.dataset = fuenteDatos

            self._coverage_properties = fuenteDatos.propiedades_cobertura()
            self.axes = self._coverage_properties['axes']
            self.crs = self._coverage_properties['bbox_crs']
            self.num_bands = self._coverage_properties['num_bands']
            self.get_fields()
            self.info = self.dataset.gdalinfo_2_json()
            format= {
                    "name": self.info['driver']['short_name'],
                    "longName": self.info['driver']['long_name'],
                    "mimetype": ""
            }
            self.native_format = self.format = format
            
            # Validación: al menos un dataset debe estar abierto
            if not self.dataset:
                raise ProviderConnectionError(f"No se pudo abrir el archivo ráster: {self.file}")

        else:
            raise ProviderQueryError(f"El valor {self.__url__} no está definido en las propiedades de la consulta")

        print('properties:', properties)
        if self.__properties__ in kwargs:
            print('kwargs[self.__properties__]')
            properties = kwargs[self.__properties__].split(',')
        if properties:
            self.dataset.extraer_bandas(bandas= properties)

        print('bbox:', bbox)
        if bbox:
            self.dataset.MRE_datos(MRE=bbox, EPSG_MRE=bbox_crs)

        elif subsets:
            if (self._coverage_properties['x_axis_label'] in subsets and
                self._coverage_properties['y_axis_label'] in subsets):

                x = self._coverage_properties['x_axis_label']
                y = self._coverage_properties['y_axis_label']

                bbox = [subsets[x][0], subsets[y][0], subsets[x][1], subsets[y][1]]
                self.dataset.MRE_datos(MRE=bbox, EPSG_MRE=bbox_crs)

            else:
                raise ProviderQueryError("Subconjunto debe incluir 'x' e 'y'")

        print('kwargs:', kwargs)
        if 'height' in kwargs or 'width' in kwargs:
            height = kwargs.get('height', None)
            width = kwargs.get('width', None)
            self.dataset.redimensionar(height=height, width=width)
            
        print('datetime:', datetime_)
        print('format:', format_)
        if format_ == 'json' or format_ == 'application/json':
            return self.dataset.exportar(outputFormat=format_)
        elif format_=='GTiff' or format_ == 'image/tiff':
            return self.dataset.exportar(outputFormat=format_)
        else:
            try:
                return self.dataset.exportar(outputFormat=format_)
            except Exception as e:
                raise ProviderQueryError(f"Formato no soportado: {format_}")

    def get(self, identifier, **kwargs):
        """
        No aplica a ráster, pero podemos implementar algo opcional (ej. pixel por ID).
        """
        raise NotImplementedError("Método get() no soportado para ráster.")

    def get_schema(self):
        """
        Devuelve el esquema esperado para la respuesta.
        """
        return ('application/json', {'description': 'Respuesta básica del ráster'})


