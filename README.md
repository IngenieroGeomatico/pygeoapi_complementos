# pygeoapi_complementos

Repositorio para añadir funcionalidades a pygeoapi.

¡¡¡¡¡En desarrollo!!!!!


export PYTHONPATH=$(pwd)

export PYGEOAPI_OPENAPI=example-openapi.yml

export PYGEOAPI_CONFIG="pygeoapi/pygeoapi_complementos/test/pygeoapi-config_OGR_DataProvider.yml"

pygeoapi openapi generate $PYGEOAPI_CONFIG --output-file $PYGEOAPI_OPENAPI

pygeoapi serve --django



URL prueba:

http://localhost:5000/collections/OGR_1/items/?f=html&__layer__=3&profundida=0.0&limit=11&bbox=-5.557022094726563,35.92075216811695,-5.331115722656251,36.050764426908515

http://localhost:5000/collections/OGR_1/items/132?__layer__=01_04_Batimetria



http://localhost:5000/collections/OGR_2_Proxy/items/?f=html&__properties__=profundida&profundida=0.0&limit=11&__layer__=3&bbox=-5.557022094726563,35.92075216811695,-5.331115722656251,36.050764426908515&__url__=https://www.juntadeandalucia.es/institutodeestadisticaycartografia/dega/sites/default/files/datos/094-dera-1-relieve.zip

http://localhost:5000/collections/OGR_2_Proxy/items/132?__layer__=01_04_Batimetria&__url__=https://www.juntadeandalucia.es/institutodeestadisticaycartografia/dega/sites/default/files/datos/094-dera-1-relieve.zip
