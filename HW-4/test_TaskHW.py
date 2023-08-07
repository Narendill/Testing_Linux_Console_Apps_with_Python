# Задание 1.
# Переделать все шаги позитивных тестов на выполнение по SSH. Проверить работу.
#
# Задание 2. (дополнительное задание)
# Переделать все шаги негативных тестов на выполнение по SSH. Проверить работу.

from checkout import getout
from sshcheckers import upload_files, ssh_checkout, ssh_checkout_negative
from pathlib import Path
import yaml


with open('config.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

TST = data['TST']
OUT = data['OUT']
FOLDER1 = data['FOLDER1']
ARX_TYPE = data['ARX_TYPE']
PASSWORD = data['PASSWORD']
USERNAME = data['USERNAME']
HOST = data['HOST']
PACKNAME = data['PACKNAME']
UPLOAD_ADDRESS = data['UPLOAD_ADDRESS']


def save_log(start_time, name):
    """Сохраняет логи."""
    if not Path('./logs').exists():
        Path('./logs').mkdir()
    with open(f'./logs/{name}', 'w', encoding='utf-8') as file:
        file.write(''.join(getout(f'journalctl --since "{start_time}"')[0]))


def test_step0(start_time):
    """Развертывание пакета 7z."""
    res = []
    # Загрузка пакета:
    upload_files(HOST, USERNAME, PASSWORD, f'{PACKNAME}', f'{UPLOAD_ADDRESS}/{PACKNAME}')
    # Установка пакета:
    res.append(ssh_checkout(HOST, USERNAME, PASSWORD, f'echo "2222" | sudo -S dpkg -i {UPLOAD_ADDRESS}/{PACKNAME}',
                            'Настраивается пакет'))
    # Проверка пакета в списке пакетов:
    res.append(ssh_checkout(HOST, USERNAME, PASSWORD, f'echo "2222" | sudo -S dpkg -s {PACKNAME.split(".")[0]}',
                 'Status: install ok installed'))
    save_log(start_time, 'log_test_step0')
    assert all(res), 'test0 FAIL'


def test_step1(clear_dir, get_dir, make_files, logger, start_time):
    """Проверка на создание архива."""
    res1 = ssh_checkout(HOST, USERNAME, PASSWORD, f'cd {TST}; 7z a {ARX_TYPE} {OUT}/arx2', 'Everything is Ok')
    res2 = ssh_checkout(HOST, USERNAME, PASSWORD, f'ls {OUT}', f'arx2.{ARX_TYPE[2:]}')
    save_log(start_time, 'log_test_step1')
    assert res1 and res2, 'test1 FAIL'


def test_step2(clear_dir, get_dir, make_files, logger, start_time):
    """Проверка на создание файла при распаковке."""
    res = []
    res.append(ssh_checkout(HOST, USERNAME, PASSWORD, f'cd {TST}; 7z a {ARX_TYPE} {OUT}/arx2',
                            'Everything is Ok'))
    res.append(ssh_checkout(HOST, USERNAME, PASSWORD, f'cd {OUT}; 7z e arx2.{ARX_TYPE[2:]} -o{FOLDER1} -y',
                            'Everything is Ok'))
    for i in make_files:
        res.append(ssh_checkout(HOST, USERNAME, PASSWORD, f'ls {FOLDER1}', i))
    save_log(start_time, 'log_test_step2')
    assert all(res), 'test2 FAIL'


def test_step3(logger, start_time):
    """Проверка архива на повереждение."""
    save_log(start_time, 'log_test_step3')
    assert ssh_checkout(HOST, USERNAME, PASSWORD, f'cd {OUT}; 7z t arx2.{ARX_TYPE[2:]}',
                        'Everything is Ok'), 'test3 FAIL'


def test_step4(get_list_files_ssh, logger, start_time):
    """Проверка удаления файла из архива."""
    save_log(start_time, 'log_test_step4')
    assert ssh_checkout(HOST, USERNAME, PASSWORD, f'cd {OUT}; 7z d arx2.{ARX_TYPE[2:]} {get_list_files_ssh[0]}',
                        'Everything is Ok'), 'test4 FAIL'



def test_step5(get_list_files_ssh, logger, start_time):
    """Проверка обновления архива."""
    save_log(start_time, 'log_test_step5')
    assert ssh_checkout(HOST, USERNAME, PASSWORD, f'cd {TST}; echo "hello" >> {get_list_files_ssh[1]}; cd {OUT};' +
                    f'7z u arx2.{ARX_TYPE[2:]} {TST}/{get_list_files_ssh[1]}', 'Everything is Ok'), 'test5 FAIL'


def test_step6(get_bad_file, logger, start_time):
    """Проверка поврежденного архива на повреждение - негативный тест."""
    save_log(start_time, 'log_test_step6')
    assert ssh_checkout_negative(HOST, USERNAME, PASSWORD, f'cd {OUT}; 7z t arx_bad.{ARX_TYPE[2:]}',
                        'Open ERROR'), 'test6 FAIL'


def test_step7(get_bad_file, logger, start_time, del_application):
    """Проверка распаковки битого архива - негативный тест. В конце удаляет 7z."""
    save_log(start_time, 'log_test_step7')
    assert ssh_checkout_negative(HOST, USERNAME, PASSWORD, f'cd {OUT}; 7z e arx_bad.{ARX_TYPE[2:]} -o{FOLDER1} -y',
                        'Open ERROR'), 'test7 FAIL'
