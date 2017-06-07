import os
from modules.my_classes.custom_functions import wrap_double_quotes as wrap

def run_dump(connection_settings: dict, path_to_pgdump: str, objects: list, type_dump: str, out_dir: str):
    host = ' -h' + wrap(connection_settings['host'])
    user = ' -U' + wrap(connection_settings['user'])
    if connection_settings['port'] == 'default':
        port = ' -p' + '5432'
    else:
        port = ' -p' + connection_settings['port']

    if type_dump == 'Only Data':
        type_d = '-a'
    elif type_dump == 'Only Schema':
        type_d = '-s'
    else:
        type_d = ''

    for obj in objects:
        tmp = obj.split('.')
        database = ' -d' + wrap(tmp[0])
        schema = ' -n' + wrap(tmp[1])
        table = ' -t' + wrap(tmp[2])
        normalize_path = os.path.normcase(out_dir + '/' + tmp[0] + '/' + tmp[1] + tmp[2])
        out_file = ' -f' + wrap(normalize_path + '.sql')
        cmd_for_run = (wrap(path_to_pgdump) + host + user + port
                       + database + schema + table + ' ' + type_d
                       + out_file)
        print(cmd_for_run)


    """
5432
"%pgdump$cmd%"
- h % Server$name %
-U % User$name %
-p % Port$number %
-d % Database %
-n % Scheme$name %
-t table_name
% Type %
-f % dir % % Scheme$name %.sql
"""