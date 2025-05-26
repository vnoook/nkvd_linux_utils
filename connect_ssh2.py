import re
import csv
import fabric
import socket
import lu_conf  # файл с доступами


# функция для проверки компа в сети и доступности на нём порта 22
def check_host_accessibility(host: str) -> bool:
    socket.setdefaulttimeout(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, 22))
    except TimeoutError as _err1:
        return False
    except Exception as _err2:
        return False
    else:
        return True
    finally:
        sock.close()

# функция для получения ip-адреса по имени компа
def get_host_ip(host: str) -> str:
    host_ip = socket.getgethostbyname(host)
    return host_ip


# функция удаления непечатаемых символов
def del_simbols(str_in: str) -> str:
    return re.sub('[\t\r\n]', '', str_in)


# переменные
file_csv = 'hosts.csv'
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

    # get_host_ip(comp)
    # exit()

    if check_host_accessibility(comp):
        conn = fabric.Connection(host=comp, user=lu_conf.user,
                                 connect_kwargs={"password": lu_conf.secret}, config=config)
        try:
            # 1
            rez = conn.run('uname -r')
            comp_dict[comp] = del_simbols(rez.stdout)
            # 2
            conn.sudo('apt-get update')
            conn.sudo('apt-get dist-upgrade -y')
            conn.sudo('update-kernel -y')
            # 3
            # conn.sudo('puppet agent -t')
            # 4
            # conn.sudo(r'/opt/cprocsp/sbin/amd64/cpconfig -ini "\config\cades\TrustedSites\TrustedSites" -delparam')
            # conn.sudo(r'/opt/cprocsp/sbin/amd64/cpconfig -ini "\config\cades\TrustedSites" -add multistring'
            #           r' "TrustedSites" "https://*.egisznso.ru" "http://*.egisznso.ru" "https://*.cryptopro.ru"'
            #           r' "http://*.cryptopro.ru" "http://dlo-app.egisznso.ru" "https://dlo-app.egisznso.ru"'
            #           r' "http://10.101.39.10" "https://10.101.39.10" "https://lk.zakupki.gov.ru"'
            #           r' "https://*.gov.ru"')

            conn.close()
        except Exception as _err:
            print('--- пароли не подходят ---', _err)
            comp_dict[comp] = del_simbols(str(_err))
        conn.close()
    else:
        print('--- не в сети или нет доступа по SSH ---')
        comp_dict[comp] = del_simbols('--- не в сети или нет доступа по SSH ---')

    print()
    print('*'*50)

for key, value in comp_dict.items():
    print(f'{key};{value}')

# for i in dir(conn):
#     if '__doc__' not in i:
#         print(f'... {i} ... {getattr(conn, i, None)}')
#         print('_' * 45)
