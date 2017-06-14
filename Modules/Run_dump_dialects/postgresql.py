import os
from Modules.my_classes import custom_functions


def get_list_of_cmd(dialect_name: str, connection_settings: dict,
                    path_to_pgdump: str,
                    objects: list,
                    type_dump: str,
                    out_dir: str):
    """
    :param dialect_name: Название диалекта (для логирования)
    :param connection_settings: Объект с парамметрами подключения
    :param path_to_pgdump: Абсолютный путь к pgdump.exe
    :param objects: Массив объектов для которых необходимо сделать ДАМП
            [database1.schema1.table1, database3.schema1.table5]
    :param type_dump: Строковое значение типа дампа "Only Data, Only Schema, Data and Schema"
    :param out_dir: Абсолютный путь к папке, в которую выгружаем файлы ДАМПов
    :return: Запускает создание дампов, используются функции: run_cmd, write_to_log
    """

    """
        default port is 5432


        "%pgdump$cmd%"
        - h % Server$name %
        -U % User$name %
        -p % Port$number %
        -d % Database %
        -n % Scheme$name %
        -t table_name
        % Type %
        -f % dir % % Scheme$name %.sql

        Второй вариант:

        "c:\program files\postgresql\9.5\bin\pg_dump.exe" 
        -h"VM-DBA-2008R2-5" 
        -U"qa" 
        -p5432 
        -s 
        -f"D:\data\from_dump\gp_approxima.sql" 
        -t"\"DBCS_D_GREENPLUM\".approximatenumerics" "DBCS_D_GREENPLUM"
    """

    host = ' -h' + custom_functions.wrap_double_quotes(connection_settings['host'])
    user = ' -U' + custom_functions.wrap_double_quotes(connection_settings['user'])
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

    list_of_cmd = []

    for obj in objects:
        tmp = obj.split('.')
        database = tmp[0]
        schema = tmp[1]
        table = tmp[2]
        normalize_outdir_path = os.path.normcase(out_dir + '/' + dialect_name + '/' + database + '/' + schema)

        # Если папки нет, создаем
        # Папка диалекта
        if not os.path.isdir(os.path.normcase(out_dir + '/' + dialect_name)):
            os.mkdir(os.path.normcase(out_dir + '/' + dialect_name))
        # Папка базы
        if not os.path.isdir(os.path.normcase(out_dir + '/' + dialect_name + '/' + database)):
            os.mkdir(os.path.normcase(out_dir + '/' + dialect_name + '/' + database))
        # Папка схемы
        if not os.path.isdir(os.path.normcase(out_dir + '/' + dialect_name + '/' + database + '/' + schema)):
            os.mkdir(os.path.normcase(out_dir + '/' + dialect_name + '/' + database + '/' + schema))

        out_file = normalize_outdir_path + '/' + table + '.sql'
        cmd_for_run = (custom_functions.wrap_double_quotes(path_to_pgdump) +
                       host +
                       user +
                       port +
                       ' ' + type_d +
                       ' -f' + custom_functions.wrap_double_quotes(out_file) +
                       ' -t' + '"' +
                       r'\"' + schema + r'\"' + '.' +
                       r'\"' + table + r'\"' +
                       '"' +
                       ' ' + '"' + database + '"'
                       )

        list_of_cmd.append([obj, cmd_for_run])
    return list_of_cmd
