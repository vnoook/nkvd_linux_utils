import fabric
import concurrent.futures
import lu_conf  # файл с доступами
import linux_utils


file_csv = 'res/hosts.csv'


def updater(comp: str) -> bool:
    host_online =  linux_utils.check_host_accessibility(comp)
    host_ip = linux_utils.get_host_ip(comp)
    comp_dict[comp] = ','.join((host_ip, ''))
    print(comp_dict)

    if host_online:
        # общий конфиг для всех соединений
        utf8en_env = {'LANG': 'en_US.UTF-8', 'LC_ALL': 'en_US.UTF-8'}
        config = fabric.Config(overrides={'sudo': {'password': lu_conf.secret, 'env': utf8en_env},
                                          'run': {'env': utf8en_env}})
        conn = fabric.Connection(host=comp, user=lu_conf.user,
                                 connect_kwargs={"password": lu_conf.secret}, config=config)
        try:
            rez = conn.sudo('uname -r', hide=True)
            # print(f'{(rez) = }')
            print(f'{(linux_utils.del_simbols(rez.stdout)) = }')
            print(f'{(linux_utils.del_simbols(rez.stderr)) = }')

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
    comp_list = linux_utils.read_file_csv(file_csv)

    print("\033[1;32m" + "Начинаю сбор данных с компьютеров ..." + "\033[0m")
    # Запуск опроса в несколько потоков для скорости
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(updater, comp_list)
    print("\033[1;32m" + "Обработка данных закончена ..." + "\033[0m")

    # for key, value in comp_dict.items():
    #     print(f'{key},{value}')


if __name__ == '__main__':
    # переменные
    comp_dict = {}

    run()
