import concurrent.futures
import paramiko
import csv
import lu_conf  # файл с доступами
import connect_ssh2 as cs2

# Настройки подключения
SSH_USER = lu_conf.user
SSH_PASSWORD = lu_conf.secret
TARGET_DIR = lu_conf.users_dir
file_csv = 'res/hosts.csv'
users_csv = 'res/users.csv'
time_out = 1


# функция чтения файла и получения из него списка имён пользователей и их секреты
def read_users_csv(users_file) -> dict:
    users_dict = {}
    # чтение файла с пользователями
    with open(users_file, encoding='cp1251', newline='') as csvfile:
        row_csv_content = csv.reader(csvfile, delimiter=',')
        for row in row_csv_content:
            users_dict[row[0]] = row[1]
    return users_dict


# функция чтения файла и получения из него списка имён компов
def read_file_csv(file) -> list:
    comp_name_list = []
    # чтение файла с адресами компов
    with open(file, encoding='cp1251', newline='') as csvfile:
        row_csv_content = csv.reader(csvfile, delimiter=',')
        next(row_csv_content)  # пропускаю первую строку
        for row in row_csv_content:
            comp_name_list.append(row[0])
    return comp_name_list


# функция получения содержимого папки с пользователями на компе host
def get_folders_from_host(host_name) -> tuple:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Подключение к хосту
        client.connect(
            hostname=host_name,
            username=SSH_USER,
            password=SSH_PASSWORD,
            timeout=time_out
        )
        # Команда выводит только имена папок (тип d) в указанной директории
        # -maxdepth 1 и -mindepth 1 исключают саму папку и вложенные подпапки
        command = f"find {TARGET_DIR} -mindepth 1 -maxdepth 1 -type d -printf '%f\\n'"
        stdin, stdout, stderr = client.exec_command(command)

        folders = stdout.read().decode("utf-8").strip().split("\n")
        errors = stderr.read().decode("utf-8").strip()

        if errors:
            # return host_name, f"Ошибка на {host_name}: {errors}"
            return host_name, ""

        # Фильтруем пустые строки, если папок нет
        folders = [f for f in folders if f]
        # return host_name, folders if folders else ["Папки не найдены или директория пуста"]
        return host_name, folders if folders else ""

    except Exception as e:
        # return host_name, f"{host_name},Не удалось подключиться к {host_name}: {str(e)}"
        return host_name, ""
    finally:
        client.close()

# функция сброса параметра ignore-host у конкретного пользователя на конкретном host
def reset_ignorehosts_host_user(host_name, user, passwrd) -> str:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Подключение к хосту
        client.connect(
            hostname=host_name,
            username=user,
            password=passwrd,
            timeout=time_out
        )
        stdin, stdout, stderr = client.exec_command("gsettings reset org.gnome.system.proxy ignore-hosts")
        ignore_hosts = stdout.read().decode("utf-8").strip().split("\n")

        errors = stderr.read().decode("utf-8").strip()
        if errors:
            return f"Ошибка сброса ignore-hosts : {errors}"

        return str(ignore_hosts[0]) if not isinstance(ignore_hosts[0], str) else ignore_hosts[0]

    except Exception as e:
        # return f"Не удалось подключиться к {host_name}: {str(e)}"
        return f"Не удалось подключиться: {str(e)}"
    finally:
        client.close()


# функция получения параметра ignore-host у конкретного пользователя на конкретном host
def get_ignorehosts_host_user(host_name, user, passwrd) -> str:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Подключение к хосту
        client.connect(
            hostname=host_name,
            username=user,
            password=passwrd,
            timeout=time_out
        )
        stdin, stdout, stderr = client.exec_command("gsettings get org.gnome.system.proxy ignore-hosts")
        ignore_hosts = stdout.read().decode("utf-8").strip().split("\n")

        errors = stderr.read().decode("utf-8").strip()
        if errors:
            return f"Ошибка: {errors}"

        return str(ignore_hosts[0]) if not isinstance(ignore_hosts[0], str) else ignore_hosts[0]

    except Exception as e:
        # return f"Не удалось подключиться к {host_name}: {str(e)}"
        return f"Не удалось подключиться: {str(e)}"
    finally:
        client.close()


def main():
    comp_list = read_file_csv(file_csv)
    users_dict = read_users_csv(users_csv)
    # comp_dict = {}

    print("\033[1;32m" + "Начинаю сбор данных с компьютеров ..." + "\033[0m")
    # Запуск опроса в несколько потоков для скорости
    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        results = executor.map(get_folders_from_host, comp_list)
    print("\033[1;32m" + "Сбор данных закончен, начинаю обработку ..." + "\033[0m")

    for host, output in results:
        # print(host+","+str(output) if output else host)
        # continue

        if isinstance(output, list):
            for folder in output:
                user_name = folder
                if user_name in users_dict.keys():
                    user_pass = users_dict[user_name]

                    cur_getignore = get_ignorehosts_host_user(host, user_name, user_pass)
                    print(host + "," + user_name + "," + cur_getignore)

                    reset_ignorehosts_host_user(host, user_name, user_pass)

                    cur_getignore = get_ignorehosts_host_user(host, user_name, user_pass)
                    print(host + "," + user_name + "," + cur_getignore)

                    # if ((cur_getignore != cs2.default_ignore_list)
                    #         and (cur_getignore != cs2.nokkvd_ignore_list)):
                    #     print(host + "," + user_name + "," + cur_getignore)
        # else:
        #     print(host + ",")


if __name__ == "__main__":
    main()

# gsettings reset org.gnome.system.proxy ignore-hosts
# gsettings get org.gnome.system.proxy ignore-hosts

    # if cs2.is_ip_address(cs2.get_host_ip(host)):
    #     # comp_dict[comp] = ', '.join((str(get_host_ip(host)), del_simbols(error_msg)))
    #     pass
    # else:
    #     # comp_dict[comp] = del_simbols(error_msg)
    #     pass
    #
    # print('*' * 50)
    # for key, value in comp_dict.items():
    #     print(f'{key},{value}')
