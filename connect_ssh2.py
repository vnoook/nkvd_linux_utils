import re
import csv
import fabric
import socket
import ipaddress
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
    try:
        host_ip = socket.gethostbyname(host)
    except Exception as _err3:
        host_ip = str(_err3)
    return host_ip


# функция определения ip адрес это или нет
def is_ip_address(str_in: str) -> bool:
    try:
        ipaddress.ip_address(str_in)
        return True
    except ValueError:
        return False


# функция удаления непечатаемых символов
def del_simbols(str_in: str) -> str:
    return re.sub('[\t\r\n]', '', str_in)


# декодирование нечитаемой информации из выводов в читаемую
def decode_output(in_result) -> str:
    correct_out_resultoutput = in_result.stdout.encode('cp1251').decode('utf-8')
    # print(correct_output)
    return out_result


# функция чтения файла и получения из него списка имён компов
def read_file_csv(file_csv) -> list:
    comp_name_list = []
    # чтение файла с адресами компов
    with open(file_csv, encoding='cp1251', newline='') as csvfile:
        row_csv_content = csv.reader(csvfile, delimiter=',')
        next(row_csv_content)  # пропускаю первую строку
        for row in row_csv_content:
            comp_name_list.append(row[0])
    return comp_name_list


# основная функция запуска приложения
def run() -> None:
    # переменные
    file_csv = 'hosts.csv'
    comp_dict = {}

    # чтение файла
    comp_list = read_file_csv(file_csv)

    # общий конфиг для всех соединений
    # config = fabric.Config(overrides={"sudo": {"password": lu_conf.secret}})
    utf8en_env = {'LANG': 'en_US.UTF-8', 'LC_ALL': 'en_US.UTF-8'}
    config = fabric.Config(overrides={'sudo': {'password': lu_conf.secret, 'env': utf8en_env},
                                      'run': {'env': utf8en_env}})
    # ***utf8ru_env = {'LANG': 'ru_RU.UTF-8', 'LC_ALL': 'ru_RU.UTF-8'}
    # ***config = fabric.Config(overrides={'sudo': {'password': lu_conf.secret, 'env': utf8ru_env},
    #                                   'run': {'env': utf8ru_env}})
    print('*' * 50)

    # цикл подключения ко всем компам из списка в файле
    for comp in comp_list:
        print(comp+',', get_host_ip(comp), end=', ')

        if check_host_accessibility(comp):
            conn = fabric.Connection(host=comp, user=lu_conf.user,
                                     connect_kwargs={"password": lu_conf.secret}, config=config)
            try:
                # 1
                rez = conn.sudo('uname -r')
                comp_dict[comp] = ', '.join((get_host_ip(comp), del_simbols(rez.stdout)))
                # 2
                # conn.sudo('apt-get update')
                # conn.sudo('apt-get dist-upgrade -y')
                # 3
                # conn.sudo('update-kernel -y')
                # 4
                # conn.sudo('remove-old-kernels -y')
                # 5
                # conn.sudo(r'/opt/cprocsp/sbin/amd64/cpconfig -ini "\config\cades\TrustedSites\TrustedSites" -delparam')
                # conn.sudo(r'/opt/cprocsp/sbin/amd64/cpconfig -ini "\config\cades\TrustedSites" -add multistring'
                #           r' "TrustedSites" "https://*.egisznso.ru" "http://*.egisznso.ru" "https://*.cryptopro.ru"'
                #           r' "http://*.cryptopro.ru" "http://*.cadescompany.ru" "http://dlo-app.egisznso.ru"'
                #           r' "https://dlo-app.egisznso.ru" "https://lk.zakupki.gov.ru" "https://*.gov.ru"'
                #           r' "http://10.101.39.10" "https://10.101.39.10"')
                # 6 -------------
                # rez_usb_devices = conn.run('lsusb')
                # 7
                conn.sudo(r'bash < <(curl -s http://alt-mirror.arm.loc/scripts/repair_hostname.sh)', warn=True)
                # 8
                conn.sudo(r'bash < <(curl -s http://alt-mirror.arm.loc/scripts/cprocsp-fix.sh)', warn=True)
                # 9
                # rez_usb_devices = conn.run('/etc/NX/nxnode --version')
                # 10
                conn.sudo('puppet agent -t', warn=True)
                # ***conn.sudo('puppet agent -t', warn=True, env={'LANG': 'en_US.UTF-8', 'LC_ALL': 'en_US.UTF-8'})
                # ***conn.sudo('puppet agent -t', warn=True, env={'LANG': 'ru_RU.UTF-8', 'LC_ALL': 'ru_RU.UTF-8'})
                # 11
                # conn.sudo('gsettings get org.gnome.system.proxy ignore-hosts')
                # 12
                # echo $DISPLAY
                # conn.sudo('echo $DISPLAY')
                # export DISPLAY=:0
                # rez2 = conn.sudo('export DISPLAY=:1.0')
                # result = conn.run('export DISPLAY=:1.0 && echo $DISPLAY')
                # conn.sudo('export DISPLAY=:1.0 && echo $DISPLAY')
                # gsettings set org.gnome.system.proxy ignore-hosts ("['localhost', '127.0.0.0/8', '::1', 'portal',"
                #                                                    "'*.egisznso.ru', '10.101.39.10']")
                # conn.sudo('gsettings set org.gnome.system.proxy ignore-hosts "[\'localhost\', \'127.0.0.0/8\','
                #           '\'::1\',\'portal\', \'*.egisznso.ru\', \'10.101.39.10\']"')
                # conn.sudo('gsettings get org.gnome.system.proxy ignore-hosts')
                # 13
                # print()
                # print('*'*46)
                # result = conn.run("ping -c 3 006-000-99-999.arm.loc", hide=False)
                # # print(f"stdout: {result.stdout = }")
                # print(f"stderr: {result.stderr = }")
                # print(f"stderr: {result.command = }")
                # print(f"stderr: {result.disowned = }")
                # print(f"stderr: {result.encoding = }")
                # print(f"stderr: {result.env = }")
                # print(f"stderr: {result.exited = }")
                # print(f"stderr: {result.failed = }")
                # print(f"stderr: {result.hide = }")
                # print(f"stderr: {result.ok = }")
                # print(f"stderr: {result.pid = }")
                # print(f"stderr: {result.pty = }")
                # print(f"stderr: {result.return_code = }")
                # print(f"stderr: {result.shell = }")
                # if result.failed:
                #     print(f"Команда завершилась с ошибкой: {result.stderr}")
                # else:
                #     print(f"Успешно выполнено. Вывод:\n{result.stdout}")

            except Exception as _err:
                print('--- пароли не подходят --- ', _err)
                comp_dict[comp] = ', '.join((get_host_ip(comp), del_simbols(str(_err))))
            conn.close()
        else:
            error_msg = '--- не в сети или нет доступа по SSH ---'
            print(error_msg)
            if is_ip_address(get_host_ip(comp)):
                comp_dict[comp] = ', '.join((str(get_host_ip(comp)), del_simbols(error_msg)))
            else:
                comp_dict[comp] = del_simbols(error_msg)
        print()
        print('*'*50)

    for key, value in comp_dict.items():
        print(f'{key},{value}')


if __name__ == '__main__':
    run()
