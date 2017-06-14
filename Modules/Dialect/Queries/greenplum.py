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
    import psycopg2
    import sys
    conn_string = get_full_con_str(obj_connection_settings)

    try:
        psycopg2.connect(conn_string)
        return 'Connected'
    except:
        return sys.exc_info()[1].args[0]



def all_databases(obj_connection_settings):
    import psycopg2
    conn_string = get_full_con_str(obj_connection_settings)
    try:
        cnct = psycopg2.connect(conn_string)
    except:
        return []
    cursor = cnct.cursor()
    sql_query = """
        SELECT datname FROM pg_catalog.pg_database
            where datname not in 
            ( 'postgres'
            , 'template0'
            , 'template1'
            , 'gpadmin'
            , 'gpperfmon'
            ) order by 1;
    """

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_arr = []

    for i in records:
        out_arr.append(i[0])

    return out_arr


def all_schemas(obj_connection_settings, database):
    import psycopg2
    conn_string = get_full_con_str(obj_connection_settings)
    try:
        cnct = psycopg2.connect(conn_string)
    except:
        return []

    cursor = cnct.cursor()
    sql_query = """
                SELECT
                  sm.nspname AS name 
                FROM
                  pg_namespace sm
                """
    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_arr = []

    for i in records:
        out_arr.append(i[0])

    return out_arr


def all_tables(obj_connection_settings, schema):
    import psycopg2
    conn_string = get_full_con_str(obj_connection_settings)
    try:
        cnct = psycopg2.connect(conn_string)
    except:
        return []
    cursor = cnct.cursor()
    sql_query = """
        SELECT
          t.relname AS name
        FROM
          pg_class t
          JOIN gp_distribution_policy gdp
            ON t.oid = gdp.localoid
          JOIN pg_namespace ns
            ON ns.oid = t.relnamespace
        WHERE
          t.relkind = 'r'
          AND t.relstorage <> 'x'
          AND NOT EXISTS (SELECT 1 FROM pg_partitions prt WHERE prt.partitiontablename = t.relname AND prt.partitionschemaname = ns.nspname)
          AND ns.nspname = '{}' 

    """.format(schema)

    cursor.execute(sql_query)
    records = cursor.fetchall()

    out_arr = []

    for i in records:
        out_arr.append(i[0])

    return out_arr