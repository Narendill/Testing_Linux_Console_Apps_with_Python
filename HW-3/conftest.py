from datetime import datetime
import random
import string
import pytest
import yaml
from checkout import checkout, getout

with open('config.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

TST = data['TST']
OUT = data['OUT']
FOLDER1 = data['FOLDER1']
ARX_TYPE = data['ARX_TYPE']


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
    return checkout(f'mkdir {TST} {OUT} {FOLDER1}', '')


@pytest.fixture()
def make_files():
    """Создание файлов."""
    list_files = []
    for i in range(data['COUNT_FILES']):
        filename = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        if checkout(f'cd {TST}; dd if=/dev/urandom of={filename}' +
                    f' bs={data["SIZE_FILE"]} count={data["COUNT_FILES"]} iflag=fullblock', ''):
            list_files.append(filename)
    return list_files


@pytest.fixture()
def clear_dir():
    """Очищение папок."""
    return checkout(f'rm -rf {TST} {OUT} {FOLDER1}', '')


@pytest.fixture()
def get_list_files():
    """Возвращает список файлов."""
    return getout(f'ls {TST}')[0]


@pytest.fixture()
def get_bad_file():
    """Создает битый файл."""
    checkout(f'cd {TST}; 7z a {ARX_TYPE} {OUT}/arx_bad', 'Everything is Ok')
    checkout(f'truncate -s 1 {OUT}/arx_bad.{ARX_TYPE[2:]}', '')
    yield
    checkout(f'rm -rf {OUT}/arx_bad.{ARX_TYPE[2:]}', '')
