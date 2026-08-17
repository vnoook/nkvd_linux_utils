import concurrent.futures
import paramiko
import csv
import lu_conf  # файл с доступами
import connect_ssh2

# Настройки подключения
SSH_USER = lu_conf.user
SSH_PASSWORD = lu_conf.secret
TARGET_DIR = lu_conf.users_dir
file_csv = 'res/hosts.csv'
users_csv = 'res/users.csv'


# функция чтения файла и получения из него списка имён пользователей и их секреты
def read_users_csv(users_file) -> dict:
    users_dict = dict()
    # чтение файла с пользователями
    with open(users_file, encoding='cp1251', newline='') as csvfile:
        row_csv_content = csv.reader(csvfile, delimiter=',')
        for row in row_csv_content:
            users_dict[row[0]] = row[1]
    return users_dict


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


# функция получения содержимого папки с пользователями на компе host
def get_folders_from_host(host):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Подключение к хосту
        client.connect(
            hostname=host,
            username=SSH_USER,
            password=SSH_PASSWORD,
            timeout=3,
        )

        # Команда выводит только имена папок (тип d) в указанной директории
        # -maxdepth 1 и -mindepth 1 исключают саму папку и вложенные подпапки
        command = f"find {TARGET_DIR} -mindepth 1 -maxdepth 1 -type d -printf '%f\\n'"
        stdin, stdout, stderr = client.exec_command(command)

        folders = stdout.read().decode("utf-8").strip().split("\n")
        errors = stderr.read().decode("utf-8").strip()

        if errors:
            return host, f"Ошибка: {errors}"

        # Фильтруем пустые строки, если папок нет
        folders = [f for f in folders if f]
        return host, folders if folders else ["Папки не найдены или директория пуста"]

    except Exception as e:
        return host, f"Не удалось подключиться: {str(e)}"
    finally:
        client.close()


# функция получения параметра ignore-host у конкретного пользователя на конкретном host
def get_ignorehosts_host_user(host, user, passwrd) -> str:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Подключение к хосту
        client.connect(
            hostname=host,
            username=user,
            password=passwrd,
            timeout=5,
        )

        command = f"gsettings get org.gnome.system.proxy ignore-hosts"
        stdin, stdout, stderr = client.exec_command(command)

        ignore_hosts = stdout.read().decode("utf-8").strip().split("\n")
        errors = stderr.read().decode("utf-8").strip()

        print(ignore_hosts)
        print(len(ignore_hosts))
        print('*'*22)
        print(errors)
        exit()

        if errors:
            return host, f"Ошибка: {errors}"

        # Фильтруем пустые строки, если папок нет
        folders = [f for f in folders if f]
        return host, folders if folders else ["Папки не найдены или директория пуста"]

    except Exception as e:
        return host, f"Не удалось подключиться: {str(e)}"
    finally:
        client.close()


def main():
    print("Начинаю сбор данных с компьютеров...\n")

    comp_list = read_file_csv(file_csv)
    users_dict = read_users_csv(users_csv)

    # Запуск опроса в несколько потоков для скорости
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(get_folders_from_host, comp_list)

    for host, output in results:
        print("=== Результат для " + "\033[1;32m" + f"{host}" + "\033[0m" + " ===")
        if isinstance(output, list):
            for folder in output:
                user_name = folder
                if user_name in users_dict:
                    user_pass = users_dict[user_name]
                    print(user_name, user_pass)
                    # print(f"  [Папка] {user_name}")
                    # print(f"    [Пользователь] {user_name}")
                    get_ignorehosts_host_user(host, user_name, user_pass)
        else:
            print(f"  {output}")
        print("-" * 40)

if __name__ == "__main__":
    main()
