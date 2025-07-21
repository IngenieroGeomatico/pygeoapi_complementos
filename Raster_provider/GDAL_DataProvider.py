from pygeoapi.provider.base import BaseProvider, ProviderQueryError, ProviderConnectionError

from ..pygdal_PG_datasource.lib.Raster_conex import FuenteDatosRaster

class GDALRasterProvider(BaseProvider):
    """Mi proveedorde datos Ráster GDAL"""

    def __init__(self, provider_def):
        """Hereda de la clase padre"""
        super().__init__(provider_def)

        self.file = provider_def['data']  # Ruta del archivo ráster
        self.collection_id = provider_def.get('name', '')  # Nombre de la colección
        self.band = provider_def.get('band')  # Banda específica (opcional)
        
        # Instancia de la clase que maneja GDAL para ráster
        fuenteDatos = FuenteDatosRaster(self.file)

        # Si se especifica una banda en el YAML
        if self.band:
            if not fuenteDatos.existe_banda(self.band):
                raise ProviderQueryError(f"La banda {self.band} no existe en {self.file}")
            fuenteDatos.leer(banda=self.band)
            self.dataset = fuenteDatos
        else:
            # Si no se especifica banda, abrir dataset completo
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
        self.native_format = provider_def['format'] = format
        
        # Validación: al menos un dataset debe estar abierto
        if not self.dataset:
            raise ProviderConnectionError(f"No se pudo abrir el archivo ráster: {self.file}")

    def __repr__(self):
        return f'<GDALProvider> {self.data}'

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

        print('properties:', properties)
        if properties:
            self.dataset.extraer_bandas(bandas= properties)

        print('subsets:', subsets)
        print('bbox:', bbox)
        if bbox:
            self.dataset.MRE_datos(MRE=bbox, EPSG_MRE=bbox_crs)
        print('bbox_crs:', bbox_crs)
        print('datetime:', datetime_)
        print('kwargs:', kwargs)
        print('format:', format_)
        if format_ == 'json' or format_ == 'application/json':
            return self.dataset.exportar(outputFormat=format_)

        return 

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


