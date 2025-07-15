# pygeoapi_complementos

Repositorio para añadir funcionalidades a pygeoapi.

¡¡¡¡¡En desarrollo!!!!!


export PYTHONPATH=$(pwd)

export PYGEOAPI_OPENAPI=example-openapi.yml

export PYGEOAPI_CONFIG="pygeoapi/pygeoapi_complementos/test/pygeoapi-config_OGR_DataProvider.yml"

pygeoapi openapi generate $PYGEOAPI_CONFIG --output-file $PYGEOAPI_OPENAPI

pygeoapi serve --django
