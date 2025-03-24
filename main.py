import csv
import fabric
import socket
import lu_conf  # файл с доступами

# функция для проверки компа в сети и доступности на нём порта 22
def check_comp_accessibility(host: str) -> bool:
    socket.setdefaulttimeout(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        host_connect = sock.connect((host, 22))
    except TimeoutError as _err1:
        # print(f'{_err1 = }', end=' = ')
        return False
    except Exception as _err2:
        # print(f'{_err2 = }', end=' = ')
        return False
    else:
        # host_info = socket.getaddrinfo(host, 22)
        sock.close()
        return True

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
    # conn = fabric.Connection(host=comp, user=lu_conf.user, connect_kwargs={"password": lu_conf.secret},
    #                          config=config, connect_timeout=33)
    print(check_comp_accessibility(comp))
    # conn.close()

    # try:
    #     conn = fabric.Connection(host=comp, user=lu_conf.user, connect_kwargs={"password": lu_conf.secret},
    #                              config=config, connect_timeout=5)
    #     print(conn.is_connected.bit_count())
    # # except TimeoutError as _err:
    # #     print('какая-то ошибка', _err)
    # except Exception as _err:
    #     print('какая-то ошибка', _err)
    # else:
    #     print(conn.is_connected.bit_count())
    #     # comp_dict[comp] = conn.run('uname -r')
    #     # conn.close()

    # for i in dir(conn):
    #     if '__doc__' not in i:
    #         print(f'... {i} ... {getattr(conn, i, None)}')
    #         print('_' * 45)
