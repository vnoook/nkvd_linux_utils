import csv
import socket

file_csv = 'res/hosts.csv'

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


def run() -> None:
    # чтение файла
    comp_list = read_file_csv(file_csv)
    print(comp_list)

if __name__ == '__main__':
    run()
