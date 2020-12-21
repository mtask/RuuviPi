from .db import *
from .common import *
from flask import current_app
import logging

logger = logging.getLogger('ruuvipi')

def grafana_table_response(datas):
    logger.info("constructing grafana table response")
    response = [{"columns": [], "rows": [], "type":"table"}]
    # generate columns
    for any_data in datas:
        for key in any_data:
            # skip sqlite id row
            if key == 'id' or key not in current_app.config['DATA_COLUMNS']:
                continue
            if key == "time":
                key_type = "datetime"
            elif isinstance(any_data[key], int) or isinstance(any_data[key], float):
                key_type = "number"
            else:
                key_type = "string"
            response[0]['columns'].append({"text":key, "type": key_type})
        break
    # generate rows
    for entry in datas:
        current_row = []
        for key in entry:
            # skip sqlite id row
            if key == 'id' or key not in current_app.config['DATA_COLUMNS']:
                continue
            current_row.append(entry[key])
        response[0]['rows'].append(current_row)
    return response

def prepare_grafana_query_data(request):
    datas = {}
    for target_dict in request['targets']:
        start_date = request['range']['from']
        end_date = request['range']['to']
        mac = target_dict['target']
        logger.debug("current tag: {}".format(mac))
        data_raw, table = get_data_time_range_and_mac(current_app.config['DATABASE'], start_date, end_date, mac)
        data = prepare_data(data_raw, table)
        datas[mac] = data
    if target_dict['type'] == 'table':
        # currently I assume that table request only includes one target so latest mac defined in loop should be OK
        return grafana_table_response(datas[mac])
    else:
        raise ValueError("Unsupported query type")
