from paramiko import SSHClient, AutoAddPolicy, RSAKey
from scp import SCPClient
from os import getenv, path
from dotenv import load_dotenv

#basedir = path.relpath(path.dirname(__file__)+"../..")
load_dotenv("../.env")

mySSHP = getenv('ssh_keygen')
mySSHK = path.relpath('../../../../.ssh/ovh.pub')

def ssh_connection():
    ssh_client = SSHClient()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    ssh_client.connect(hostname='193.70.84.157',
                        username='ubuntu',
                        password=mySSHP,
                        key_filename=mySSHK)
    return ssh_client

def ssh_command(cmd):
    ssh_client = ssh_connection()
    stdin, stdout, stderr = ssh_client.exec_command(cmd)

    out = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    if out:
        return out
    if error:
        ssh_client.close()
        raise Exception('There was an error pulling the runtime: {}'.format(error))

def scp_connection():
    return SCPClient(ssh_connection().get_transport())

def scp_upload(file_to_move, path_to_directory='./mirori_faces/'):
    scp = scp_connection()
    scp.put(file_to_move, path_to_directory)

def scp_download(file_to_dl, directory):
    if file_to_dl.find('*') != -1:
        files = ssh_command("ls "+file_to_dl)
        i=0
        for file in files.split("\n"):
            scp = scp_connection()
            scp.get(file, directory)
            i+=1
    else:
        scp = scp_connection()
        scp.get(file_to_dl, directory)