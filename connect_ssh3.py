import concurrent.futures
import paramiko
import csv
import lu_conf  # файл с доступами

# Настройки подключения
SSH_USER = lu_conf.user
SSH_PASSWORD = lu_conf.secret
TARGET_DIR = lu_conf.users_dir
file_csv = 'hosts.csv'


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


def get_folders_from_host(host):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Подключение к хосту
        client.connect(
            hostname=host,
            username=SSH_USER,
            password=SSH_PASSWORD,
            timeout=5,
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


def main():
    print("Начинаю сбор данных с компьютеров...\n")

    comp_list = read_file_csv(file_csv)

    # Запуск опроса в несколько потоков для скорости
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(get_folders_from_host, comp_list)

    # Вывод результатов
    for host, output in results:
        print(f"=== Результат для {host} ===")
        if isinstance(output, list):
            for folder in output:
                print(f"  [Папка] {folder}")
        else:
            print(f"  {output}")
        print("-" * 40)


if __name__ == "__main__":
    main()
