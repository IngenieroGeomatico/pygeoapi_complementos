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



http://localhost:5000/collections/GDAL_1/coverage/?f=json&bbox=-2.782547,39.874692,-2.654154,39.928574

http://localhost:5000/collections/GDAL_2/coverage/?f=json&properties=1,2&bbox=-0.910999,39.620842,-0.909246,39.62195

http://localhost:5000/collections/GDAL_2/coverage?f=json&subset=x(-0.910999:-0.909246),y(39.620842:39.621950)

http://localhost:5000/collections/GDAL_2/coverage/?f=json&properties=1,2&subset=x(-0.910999:-0.909246),y(39.620842:39.621950)

http://localhost:5000/collections/GDAL_2/coverage/?f=json&height=10&width=10&properties=1,2&subset=x(-0.910999:-0.909246),y(39.620842:39.621950)

http://localhost:5000/collections/GDAL_2/coverage/?f=GTiff&height=10&width=10&properties=1,2&subset=x(-0.910999:-0.909246),y(39.620842:39.621950)

http://localhost:5000/collections/GDAL_PROXY/coverage/?f=json&height=10&width=10&bbox=-0.910999,39.620842,-0.909246,39.62195&__properties__=1,2&__url__=https://rapidmapping-viewer.s3.eu-west-1.amazonaws.com/EMSR773/AOI33/GRA_PRODUCT/EMSR773_AOI33_GRA_PRODUCT_PLEIADES_20241111_1120_ORTHO.tif
