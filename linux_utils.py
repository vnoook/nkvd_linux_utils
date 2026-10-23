import re
import csv
import fabric
import socket
import concurrent.futures
import lu_conf  # файл с доступами


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
