import os
def find_file_in_dir(start_dir=None, file=None):
    # print(os.getenv('SystemDrive'))
    sys_drive = os.getenv('SystemDrive')
    print(os.listdir(sys_drive))






find_file_in_dir()