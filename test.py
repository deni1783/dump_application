import os
def find_file_in_dir(start_dir=None, file=None):
    root = os.walk(start_dir)

    for d in root:
        print(d)





# find_file_in_dir(r'/_Main_folder/WORK')

root = os.walk('/Users/denissopko')
# print(root)
file = 'SOPKO DENYS.pdf'

def test():
    for path, dir, files in root:
        for f in files:
            if f == file:
                out_path = os.path.join(path, f)
                return os.path.normcase(out_path)

print(test())