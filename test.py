import os
def get_path_to_file(start_dir, file_name):
    root = os.walk(start_dir)
    for path, dir, files in root:
        for f in files:
            if f == file_name:
                out_path = os.path.join(path, f)
                return os.path.normcase(out_path)

print(get_path_to_file('C:\\', 'pg_dump.exe'))