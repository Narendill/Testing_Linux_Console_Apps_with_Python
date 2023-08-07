from datetime import datetime
import random
import string
import pytest
import yaml
from checkout import checkout, getout
import subprocess
from sshcheckers import ssh_checkout, ssh_getout

with open('config.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

TST = data['TST']
OUT = data['OUT']
FOLDER1 = data['FOLDER1']
ARX_TYPE = data['ARX_TYPE']
PACKNAME = data['PACKNAME']
PASSWORD = data['PASSWORD']
USERNAME = data['USERNAME']
HOST = data['HOST']


@pytest.fixture()
def del_application():
    """Удаление приложения."""
    # if checkout('dpkg --get-selections | grep p7zip-full', 'deinstall') or
    result = subprocess.run(f'dpkg --get-selections | grep {PACKNAME.split(".")[0]}', shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    yield
    if 'deinstall' not in result.stdout or result.stdout != '':
        checkout(f'echo "1111" | sudo -S dpkg -r {PACKNAME.split(".")[0]}', 'Удаляется p7zip-full')

@pytest.fixture()
def start_time():
    """Вовзвращает текущее время."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@pytest.fixture()
def logger():
    """После каждого шага теста дописывает в заранее созданный файл stat.txt строку вида:
    время, кол-во файлов из конфига, размер файла из конфига, статистика загрузки процессора из файла."""
    with open('stat.txt', 'a', encoding='utf-8') as file:
        file.write(f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")[:-3]} - COUNT_FILES: {data["COUNT_FILES"]} - '
                   f'SIZE_FILE: {data["SIZE_FILE"]} - STATISTIC: {getout(f"cd /proc; cat loadavg")[0]}\n')


@pytest.fixture()
def get_dir():
    """Создание папки."""
    return ssh_checkout(HOST, USERNAME, PASSWORD, f'mkdir {TST} {OUT} {FOLDER1}', '')


@pytest.fixture()
def make_files():
    """Создание файлов."""
    list_files = []
    for i in range(data['COUNT_FILES']):
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        if ssh_checkout(HOST, USERNAME, PASSWORD, f'cd {TST}; dd if=/dev/urandom of={filename}' +
                    f' bs={data["SIZE_FILE"]} count={data["COUNT_FILES"]} iflag=fullblock', ''):
            list_files.append(filename)
    return list_files


@pytest.fixture()
def clear_dir():
    """Очищение папок."""
    return ssh_checkout(HOST, USERNAME, PASSWORD, f'rm -rf {TST} {OUT} {FOLDER1}', '')


@pytest.fixture()
def get_list_files():
    """Возвращает список файлов."""
    return getout(f'ls {TST}')[0]

@pytest.fixture()
def get_list_files_ssh():
    """Возвращает список файлов на удаленной машине."""
    return ssh_getout(HOST, USERNAME, PASSWORD, f'ls {TST}')


@pytest.fixture()
def get_bad_file():
    """Создает битый файл."""
    ssh_checkout(HOST, USERNAME, PASSWORD, f'cd {TST}; 7z a {ARX_TYPE} {OUT}/arx_bad', 'Everything is Ok')
    ssh_checkout(HOST, USERNAME, PASSWORD, f'truncate -s 1 {OUT}/arx_bad.{ARX_TYPE[2:]}', '')
    # yield
    # ssh_checkout(HOST, USERNAME, PASSWORD, f'rm -rf {OUT}/arx_bad.{ARX_TYPE[2:]}', '')
