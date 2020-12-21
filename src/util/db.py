import sqlite3
from sqlite3 import Error
import logging
import datetime as dt
from datetime import timezone

logger = logging.getLogger('ruuvipi')

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.debug('created database connection to file "{}"'.format(db_file))
        return conn
    except Error as e:
        raise e

    return conn


def get_data_time_range_and_mac_internal(conn, start, end, mac):
    try:
        c = conn.cursor()
        logging.debug('Querying data: SELECT * FROM ruuvidata WHERE mac="{}" AND time BETWEEN {} AND {}'.format(mac, start, end))
        c.execute('SELECT * FROM ruuvidata WHERE mac=(?) AND time BETWEEN (?) AND (?)', [mac, start, end])
        data = c.fetchall()
        table = list(map(lambda x: x[0], c.description))
        return data,table
    except Error as e:
        logger.error(e)


def get_data_time_range_and_mac(database, start, end, mac):
    conn = create_connection(database)
    try:
        data = get_data_time_range_and_mac_internal(conn, start, end, mac)
    except Exception as e:
        raise e
    finally:
        if conn:
            conn.close()
    return data

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_tag_data(conn, data):
    c = conn.cursor()
    c.execute("INSERT INTO ruuvidata VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [dt.datetime.now(timezone.utc).isoformat(), data['data_format'], data['humidity'], data['temperature'], data['pressure'], data['acceleration'], data['acceleration_x'], data['acceleration_y'], data['acceleration_z'], data['tx_power'], data['battery'], data['movement_counter'], data['measurement_sequence_number'], data['mac']])
    conn.commit()
    logging.debug('inserting tag data to database')

def store_ruuvi_data(database, mac, tagdata):
    sql_create_ruuvidata_table = """ CREATE TABLE IF NOT EXISTS ruuvidata (
                                        id integer PRIMARY KEY,
                                        time timestamp,
                                        data_format integer,
					humidity real,
					temperature real,
					pressure real,
					acceleration real,
					acceleration_x integer,
					acceleration_y integer,
					acceleration_z integer,
					tx_power integer,
					battery integer,
					movement_counter integer,
					measurement_sequence_number integer,
					mac text
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        try:
            logging.debug('created ruuvidata table "{}" if it doesn\'t exists'.format(database))
            create_table(conn, sql_create_ruuvidata_table)
            insert_tag_data(conn, tagdata)
        except Error as e:
            logging.error(e)
        finally:
            conn.close()
    else:
        logging.error("Error! cannot create the database connection.")

