from ruuvitag_sensor.ruuvi import RuuviTagSensor
from util.db import store_ruuvi_data
import threading
import time
import logging

logger = logging.getLogger('ruuvipi')

def get_tag_data(temp_macs):
    macs = []
    for mac in temp_macs:
        # convert 1234567890 -> 12:34:45:78:90
        macs.append(':'.join(format(s, '02x') for s in bytes.fromhex(mac)).upper())
    timeout_in_sec = 20
    datas = RuuviTagSensor.get_data_for_sensors(macs, timeout_in_sec)
    logger.debug('collected data: "{}"'.format(str(datas)))
    return datas[macs[0]]

def ruuvitag_worker(mac, delay, db):
    logger.info('starting ruuvitag worker: delay "{}", mac "{}", database "{}"'.format(delay, mac, db))
    work_time = delay
    while True:
        if work_time == 0:
            logger.debug('fetching data of tag "{}"'.format(mac))
            data = get_tag_data([mac])
            logger.debug('fetced data of tag "{}"'.format(mac))
            store_ruuvi_data(db, mac, data)
            logger.debug('stored data of tag "{}"'.format(mac))
            work_time = delay
        time.sleep(1)
        work_time -= 1

def start_ruuvi_workers(tags, delay, database):
    for tag in tags:
        ruuviworker = threading.Thread(target=ruuvitag_worker, args=(tag['value'], delay, database,))
        ruuviworker.daemon = True
        ruuviworker.start()
