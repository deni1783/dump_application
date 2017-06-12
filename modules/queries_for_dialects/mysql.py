import pymysql
import sys

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
    # Пока будет так, для подключения нужно юзать пароль pwd
    obj_connection_settings['password'] = 'pwd'

    try:
        pymysql.connect(**obj_connection_settings)
        return 'Connected'
    except:
        return sys.exc_info()[1].args[1]




def all_databases(obj_connection_settings):
    pass


def all_tables(obj_connection_settings, schema):
    # Пока будет так, для подключения нужно юзать пароль pwd
    obj_connection_settings['password'] = 'pwd'

    try:
        cnct = pymysql.connect(**obj_connection_settings)
    except:
        return []

    cursor = cnct.cursor()
    sql_query = """
            SELECT 
              table_name
            FROM information_schema.tables
            WHERE table_type != 'VIEW'
              AND table_schema = '{}';
        """.format(schema)

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_obj = []

    for i in records:
        out_obj.append(i[0])
    return out_obj



def all_schemas(obj_connection_settings, empty=None):
    # Пока будет так, для подключения нужно юзать пароль pwd
    obj_connection_settings['password'] = 'pwd'

    try:
        cnct = pymysql.connect(**obj_connection_settings)
    except:
        return []

    cursor = cnct.cursor()
    sql_query = """
            SELECT 
              schema_name AS name
            FROM 
              information_schema.SCHEMATA  
        """

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_obj = []

    for i in records:
        out_obj.append(i[0])
    return out_obj

