import csv
import fabric
import socket
import lu_conf  # файл с доступами

def check_comp_accessibility(computer: str) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((computer, 22))
    print(result)
    if result == 0:
        return True
    else:
        return False

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
