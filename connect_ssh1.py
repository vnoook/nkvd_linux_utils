import re
import csv
import fabric
import socket
import concurrent.futures
import lu_conf  # файл с доступами


file_csv = 'res/hosts.csv'


# функция для получения ip-адреса по имени компа
def get_host_ip(host: str) -> str:
    try:
        host_ip = socket.gethostbyname(host)
    except Exception as _err3:
        host_ip = str(_err3)
    return host_ip


# функция удаления непечатаемых символов
def del_simbols(str_in: str) -> str:
    return re.sub('[\t\r\n]', '', str_in)


# функция чтения файла и получения из него списка имён компов
def read_file_csv(file_csv_name) -> list:
    comp_name_list = []
    # чтение файла с адресами компов
    with open(file_csv_name, encoding='cp1251', newline='') as csvfile:
        row_csv_content = csv.reader(csvfile, delimiter=',')
        next(row_csv_content)  # пропускаю первую строку
        for row in row_csv_content:
            comp_name_list.append(row[0])
    return comp_name_list


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


def updater(comp: str) -> bool:
    host_accessibility =  check_host_accessibility(comp)
    comp_dict[comp] = ','.join((get_host_ip(comp), ''))
    # comp_dict[comp] = ','.join((get_host_ip(comp), del_simbols(rez.stdout)))

    if host_access:
        # общий конфиг для всех соединений
        utf8en_env = {'LANG': 'en_US.UTF-8', 'LC_ALL': 'en_US.UTF-8'}
        config = fabric.Config(overrides={'sudo': {'password': lu_conf.secret, 'env': utf8en_env},
                                          'run': {'env': utf8en_env}})
        conn = fabric.Connection(host=comp, user=lu_conf.user,
                                 connect_kwargs={"password": lu_conf.secret}, config=config)
        try:
            rez = conn.sudo('uname -r')
            print(rez)
            print(rez.stdout)
            print(rez.stderr)

            # rez = conn.sudo('uname -r', hide=True)
            # conn.sudo('apt-get update', hide=True)
            # conn.sudo('apt-get dist-upgrade -y', hide=True)
            # conn.sudo('update-kernel -y', hide=True)
            # conn.sudo('remove-old-kernels -y', hide=True)
        except Exception as _err:
            print(f'--- на компьютере {comp} ошибка {_err} ---')
        conn.close()
    return True


def run() -> None:
    # чтение файла с компами
    comp_list = read_file_csv(file_csv)

    print("\033[1;32m" + "Начинаю сбор данных с компьютеров ..." + "\033[0m")
    # Запуск опроса в несколько потоков для скорости
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(updater, comp_list)
    print("\033[1;32m" + "Обработка данных закончена ..." + "\033[0m")

    # for key, value in comp_dict.items():
    #     print(f'{key},{value}')

    # for res in results:
    #     print(f'{res = }')


if __name__ == '__main__':
    # переменные
    comp_dict = {}

    run()
