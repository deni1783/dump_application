from subprocess import PIPE, Popen
import paramiko


def run_cmd(cmd):
    start = Popen(cmd, stdout=PIPE, shell=True)
    stdout_data, stderr_data = start.communicate()
    error_code = start.returncode
    return error_code




def test_ssh(host):
    # host = '192.168.13.153'
    user = 'nz'
    secret = 'nz'
    port = 22

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=secret, port=port)
    stdin, stdout, stderr = client.exec_command('ls')
    data = stdout.read()
    client.close()
    return data