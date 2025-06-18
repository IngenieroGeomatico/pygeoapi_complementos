
from pygeoapi.provider.base import BaseProvider, ProviderQueryError

class OGVectorProxyProvider(BaseProvider):
    """Proveedor vectorial remoto dinámico"""

    def __init__(self, provider_def):
        super().__init__(provider_def)

        # Parámetros básicos
        self.collection_id = provider_def.get('name', '') 
        self.layer = provider_def.get('layer', None)
        self.file = None  # Se define luego dinámicamente
        self.dataset = None  # dataset

    def _load_remote_file(self, url):
        """Descarga y abre el archivo remoto temporalmente con fiona"""
        suffix = self._guess_suffix(url)

        tmpfile = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            raise ProviderQueryError(f"Error al descargar el archivo: {r.status_code}")
        tmpfile.write(r.content)
        tmpfile.flush()
        tmpfile.close()

        self.file = tmpfile.name
        return self.file

    def _guess_suffix(self, url):
        if url.endswith('.geojson') or url.endswith('.json'):
            return '.geojson'
        elif url.endswith('.gpkg'):
            return '.gpkg'
        elif url.endswith('.kml'):
            return '.kml'
        else:
            return '.data'

    def _open_dataset(self, path, layer=None):
        """Abre el dataset con la capa adecuada"""
        try:
            available_layers = fiona.listlayers(path)
        except Exception as e:
            raise ProviderQueryError(f"No se pudo leer el archivo: {e}")

        # Lógica para seleccionar la capa
        if not layer:
            if '__layer__' in self.collection_id:
                layer = self.collection_id.split('__layer__', 1)[1]
            elif hasattr(self, 'layer') and self.layer in available_layers:
                layer = self.layer
            else:
                layer = available_layers[0]

        try:
            self.dataset = fiona.open(path, layer=layer)
        except Exception as e:
            raise ProviderQueryError(f"No se pudo abrir la capa '{layer}': {e}")

    def query(self, url=None, layer=None, offset=0, limit=10, **kwargs):
        """Carga datos remotos al vuelo"""

        if not url:
            raise ProviderQueryError("Falta el parámetro obligatorio ?url=")

        filepath = self._load_remote_file(url)
        self._open_dataset(filepath, layer=layer)

        features = []
        for i, feat in enumerate(self.dataset):
            if i < offset:
                continue
            if len(features) >= limit:
                break
            features.append(feat)

        return {
            "type": "FeatureCollection",
            "features": features,
            "numberMatched": len(self.dataset),
            "numberReturned": len(features)
        }

    def get(self, identifier):
        raise ProviderQueryError("No implementado: acceso por ID no soportado en modo proxy")

    def get_fields(self):
        if not self.dataset:
            return {}
        return {
            field: str(dtype)
            for field, dtype in self.dataset.schema['properties'].items()
        }

    def get_schema(self):
        return ('application/geo+json', {'$ref': 'https://geojson.org/schema/Feature.json'})
