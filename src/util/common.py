import dateutil.parser as dp
import logging

logger = logging.getLogger('ruuvipi')

def prepare_data(values, keys):
    data = []
    for row in values:
        current = {}
        for value,key in zip(row, keys):
            current[key] = value
        data.append(current)
    return data

