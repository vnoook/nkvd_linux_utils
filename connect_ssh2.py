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
    try:
        # host_ip = (socket.getaddrinfo(host, 8000))
        # print(host_ip[0][4][0])
        host_ip = socket.gethostbyname(host)
        # socket.close()
    except Exception as _err3:
        # print('--- не могу найти комп ---', _err3)
        host_ip = _err3
    return host_ip


# функция удаления непечатаемых символов
def del_simbols(str_in: str) -> str:
    return re.sub('[\t\r\n]', '', str_in)


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
    config = fabric.Config(overrides={"sudo": {"password": lu_conf.secret}})

    print('*' * 50)

    # цикл подключения ко всем компам из списка в файле
    for comp in comp_list:
        print(comp+',', get_host_ip(comp), end=', ')

        if check_host_accessibility(comp):
            conn = fabric.Connection(host=comp, user=lu_conf.user,
                                     connect_kwargs={"password": lu_conf.secret}, config=config)
            try:
                # 1
                rez = conn.run('uname -r')
                # comp_dict[comp] = get_host_ip(comp) + comp_dict[comp] + del_simbols(rez.stdout)
                print(f'{comp_dict[comp] = } ... {del_simbols(rez.stdout) = }')
                # comp_dict[comp] = str(comp_dict[comp]) + del_simbols(rez.stdout)
                # 2
                conn.sudo('apt-get update')
                conn.sudo('apt-get dist-upgrade -y')
                conn.sudo('update-kernel -y')
                # 3
                # res1 = conn.sudo('puppet agent -t', warn=True)
                # 4
                # conn.sudo(r'/opt/cprocsp/sbin/amd64/cpconfig -ini "\config\cades\TrustedSites\TrustedSites" -delparam')
                # conn.sudo(r'/opt/cprocsp/sbin/amd64/cpconfig -ini "\config\cades\TrustedSites" -add multistring'
                #           r' "TrustedSites" "https://*.egisznso.ru" "http://*.egisznso.ru" "https://*.cryptopro.ru"'
                #           r' "http://*.cryptopro.ru" "http://*.cadescompany.ru" "http://dlo-app.egisznso.ru"'
                #           r' "https://dlo-app.egisznso.ru" "https://lk.zakupki.gov.ru" "https://*.gov.ru"'
                #           r' "http://10.101.39.10" "https://10.101.39.10"')
                # 5
                # conn.run(r'bash < <(curl -s http://alt-mirror.arm.loc/scripts/repair_hostname.sh)', warn=True)
                # conn.sudo(r'bash < <(curl -s http://alt-mirror.arm.loc/scripts/repair_hostname.sh)', warn=True)
                # 6
                # conn.run(r'bash < <(curl -s http://alt-mirror.arm.loc/scripts/cprocsp-fix.sh)', warn=True)
                # conn.sudo(r'bash < <(curl -s http://alt-mirror.arm.loc/scripts/cprocsp-fix.sh)')
                # 7
                conn.sudo('remove-old-kernels -y')
                # 8
                # rez_usb_devices = conn.run('lsusb')
                # 9
                # rez_usb_devices = conn.run('/etc/NX/nxnode --version')
                # 10
                # conn.sudo('gsettings get org.gnome.system.proxy ignore-hosts')
                # 11
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
                # 12
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
                comp_dict[comp] = del_simbols(str(_err))
            conn.close()
        else:
            error_msg = '--- не в сети или нет доступа по SSH ---'
            print(error_msg)
            comp_dict[comp] = del_simbols(error_msg)

        print()
        print('*'*50)

    for key, value in comp_dict.items():
        print(f'{key},{value}')


if __name__ == '__main__':
    run()
