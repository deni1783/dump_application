import cx_Oracle
import sys
import psycopg2

def make_dns(obj):
    host = str(obj['host'])
    port = str(obj['port'])
    database = obj['database']
    return cx_Oracle.makedsn(host, port, database)

# Получить готовую строку подключения
def get_full_con_str(obj):
    con_str = ''
    host = obj['host']
    # port = obj_connection_settings['port']
    user = obj['user']
    password = obj['password']
    database = obj['database']

    if host and host != '[defaul]':
        tmp_str = 'host=' + "'" + host + "'"
        con_str += tmp_str

    if user and user != '[defaul]':
        tmp_str = ' user=' + "'" + user + "'"
        con_str += tmp_str

    if password and password != '[defaul]':
        tmp_str = ' password=' + "'" + password + "'"
        con_str += tmp_str

    if database and database != '[defaul]':
        tmp_str = ' dbname=' + "'" + database + "'"
        con_str += tmp_str
    return con_str


def connect(obj_connection_settings):
    user = obj_connection_settings['user']
    password = str(obj_connection_settings['password'])
    dsnStr = make_dns(obj_connection_settings)
    try:
        cx_Oracle.connect(user=user, password=password, dsn=dsnStr)
        return 'Connected'
    except:
        return str(sys.exc_info()[1])


def all_databases(obj_connection_settings):
    pass



def all_tables(obj_connection_settings, schema):
    dsnStr = make_dns(obj_connection_settings)
    try:
        cnct = cx_Oracle.connect(user=obj_connection_settings['user'],
                                 password=obj_connection_settings['password'],
                                 dsn=dsnStr)
    except:
        return []
    cursor = cnct.cursor()
    sql_query = """
            SELECT t.table_name
              FROM all_tables t
            WHERE t.owner = '{}'
    """.format(schema)

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_arr = []

    for i in records:
        out_arr.append(i[0])

    return out_arr


def all_schemas(obj_connection_settings, database=None):
    dsnStr = make_dns(obj_connection_settings)

    try:
        cnct = cx_Oracle.connect(user=obj_connection_settings['user'],
                                 password=obj_connection_settings['password'],
                                 dsn=dsnStr)
    except:
        return []
    cursor = cnct.cursor()
    sql_query = """
             SELECT
                usrs.username AS name
            FROM
                all_users usrs
        """

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_arr = []

    for i in records:
        out_arr.append(i[0])
    return out_arr

