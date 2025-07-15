# random_number_process.py

import logging
from pygeoapi.process.base import BaseProcessor, ProcessorExecuteError

import random

LOGGER = logging.getLogger(__name__)

#: Process metadata and description
PROCESS_METADATA = {
    'version': '0.2.0',
    'id': 'random_numbers',
    'title': {
        'en': 'Random Numbers',
    },
    'description': {
        'en': 'random numbers between two numbers',
    },
    'jobControlOptions': ['sync-execute', 'async-execute'],
    'keywords': ['hello world', 'random', 'numers'],
    'links': [{
        'type': 'text/html',
        'rel': 'about',
        'title': 'information',
        'href': 'https://example.org/process',
        'hreflang': 'en-US'
    }],
    'inputs': {
        'min': {
            'title': 'mínimo',
            'description': 'min number, by default 0',
            'schema': {
                'type': 'integer'
            },
            'minOccurs': 1,
            'maxOccurs': 1,
            'keywords': ['full name', 'personal']
        },
        'max': {
            'title': 'máximo',
            'description': 'max number, by default 100',
            'schema': {
                'type': 'integer'
            },
            'minOccurs': 0,
            'maxOccurs': 1,
            'keywords': ['message']
        }
    },
    'outputs': {
        'number': {
            'title': 'salida',
            'description': 'number result',
            'schema': {
                'type': 'object',
                'contentMediaType': 'application/json'
            }
        }
    },
    'example': {
        'inputs': {
            'min': 0,
            'max': 100,
        }
    }
}


class RandomNumberProcessor(BaseProcessor):
    """Devuelve un número aleatorio entre dos valores dados"""

    def __init__(self, provider_def):
        super().__init__(provider_def, PROCESS_METADATA)
        self.supports_outputs = True
        self.name = "random_numbers"

    def execute(self, data: dict, outputs: dict = None) -> dict:

        try:
            min_val = data.get('min', 0)
            max_val = data.get('max', 100)
            result = random.uniform(float(min_val), float(max_val))
            outputs = {
                'result': int(result),
                'input_range': [min_val, max_val]
            }
            
            mimetype = 'application/json'
            return mimetype, outputs
             
        except Exception as err:
            raise ProcessorExecuteError(f'Error ejecutando el proceso: {err}')

    def __repr__(self):
        return f'<RandomNumberProcessor> {self.name}'

