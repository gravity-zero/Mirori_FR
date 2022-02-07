import sys
sys.path.append('home/gravity/Bureau/IOT/MIRORI_FR/services')

from services import ssh 

value = ssh.ssh_command("ls")

print(value)