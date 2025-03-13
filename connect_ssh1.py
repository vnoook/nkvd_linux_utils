#!/usr/bin/python
import paramiko
import lu_conf

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=lu_conf.host, username=lu_conf.user, password=lu_conf.secret, port=lu_conf.port)

channel = client.get_transport().open_session()
channel.get_pty()
channel.settimeout(5)
channel.exec_command('su -')
channel.send(secret+'\n')
print(channel.recv(1024))

channel.close()
client.close()

# stdin, stdout, stderr = client.exec_command('ls -l')
# data = stdout.read() + stderr.read()
# print(data)
# client.close()

# client = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect(host, username=user, password=secret)
# client.exec_command('sudo -i; reboot')
# client.exec_command('sudo -i')
# client.exec_command('apt-get update')
# client.exec_command('apt-get dist-upgrade')
# client.exec_command('reboot')
# client.close()

# result = conn.run('hostnamectl | grep -i kernel')
# print(result.stdout.split(': ',2)[1])
# result = conn.run('uname -r')
# print(result.stdout)
# conn.sudo('reboot')
