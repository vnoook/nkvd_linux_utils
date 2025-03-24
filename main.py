import csv
import fabric
import socket
import lu_conf  # файл с доступами

# функция для проверки компа в сети и доступности на нём порта 22
def check_host_accessibility(host: str) -> bool:
    socket.setdefaulttimeout(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_connect = sock.connect((host, 22))
    except TimeoutError as _err1:
        return False
    except Exception as _err2:
        return False
    else:
        return True
    finally:
        sock.close()

# переменные
file_csv = 'hosts-2025-03-24.csv'
comp_dict = {}

# чтение файла с адресами компов
with open(file_csv, encoding='cp1251', newline='') as csvfile:
    row_csv_content = csv.reader(csvfile, delimiter=',')
    next(row_csv_content)  # пропускаю первую строку
    for row in row_csv_content:
        comp_dict[row[0]] = ''

# общий конфиг для всех соединений
config = fabric.Config(overrides={"sudo": {"password": lu_conf.secret}})

# цикл подключения ко всем компам из списка в файле
for comp in comp_dict:
    print(comp, end=' = ')
    if check_host_accessibility(comp):
        conn = fabric.Connection(host=comp, user=lu_conf.user, connect_kwargs={"password": lu_conf.secret}, config=config)
        # comp_dict[comp] = conn.run('uname -r')
        conn.sudo("systemctl restart cups.service")
        # print(comp_dict[comp])
        conn.close()
    else:
        print('------')



# for i in dir(conn):
#     if '__doc__' not in i:
#         print(f'... {i} ... {getattr(conn, i, None)}')
#         print('_' * 45)
