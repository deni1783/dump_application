import sys
import psycopg2

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
    try:
        psycopg2.connect(**obj_connection_settings)
        return 'Connected'
    except:
        return sys.exc_info()[1].args[0]


def all_databases(obj_connection_settings):
    pass



def all_tables(obj_connection_settings, schema):
    try:
        cnct = psycopg2.connect(**obj_connection_settings)
    except:
        return []
    cursor = cnct.cursor()
    sql_query = """
        SELECT  
           c.relname AS name
           FROM 
             pg_namespace nc
             inner join pg_class c on c.relnamespace = nc.oid
             inner join  pg_user u on u.usesysid = c.relowner
             left join pg_catalog.pg_attribute a  ON c.oid = a.attrelid  and a.attisdistkey = 1
           WHERE 
             c.relkind = 'r'
           AND nc.nspname = '{}';
    """.format(schema)

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_arr = []

    for i in records:
        out_arr.append(i[0])

    return out_arr


def all_schemas(obj_connection_settings, database=None):
    # import psycopg2
    # conn_string = get_full_con_str(obj_connection_settings)
    try:
        cnct = psycopg2.connect(**obj_connection_settings)
    except:
        return []
    cursor = cnct.cursor()
    sql_query = """
             select 
                n.nspname as name
              from pg_namespace n;
        """

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_arr = []

    for i in records:
        out_arr.append(i[0])
    return out_arr

