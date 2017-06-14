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
    return 'Connected'


def all_databases(obj_connection_settings):


    out_obj = ['dummy_database1', 'dummy_database2', 'dummy_database3', 'dummy_database4', 'dummy_database5']


    return out_obj


def all_tables(obj_connection_settings, schema):
    out_arr = ['dummy_table1', 'dummy_table2', 'dummy_table3', 'dummy_table4', 'dummy_table5', 'dummy_table6', 'dummy_table7']

    return out_arr


def all_schemas(obj_connection_settings, database):
    out_arr = ['dummy_schema1', 'dummy_schema2', 'dummy_schema3', 'dummy_schema4']

    return out_arr

