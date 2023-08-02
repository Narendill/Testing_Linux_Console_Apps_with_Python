# Задание 1.
# Дополнить проект фикстурой, которая после каждого шага теста дописывает в заранее созданный файл stat.txt строку вида:
# время, кол-во файлов из конфига, размер файла из конфига, статистика загрузки процессора из файла /proc/loadavg
# (можно писать просто всё содержимое этого файла).
#
# Задание 2. (дополнительное задание)
# Дополнить все тесты ключом команды 7z -t (тип архива). Вынести этот параметр в конфиг.

from checkout import checkout
import yaml


with open('config.yaml', 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)

TST = data['TST']
OUT = data['OUT']
FOLDER1 = data['FOLDER1']
ARX_TYPE = data['ARX_TYPE']


def test_step1(clear_dir, get_dir, make_files, logger):
    """Проверка на создание архива."""
    res1 = checkout(f'cd {TST}; 7z a {ARX_TYPE} {OUT}/arx2', 'Everything is Ok')
    res2 = checkout(f'ls {OUT}', f'arx2.{ARX_TYPE[2:]}')
    assert res1 and res2, 'test1 FAIL'


def test_step2(clear_dir, get_dir, make_files, logger):
    """Проверка на создание файла при распаковке."""
    res = []
    res.append(checkout(f'cd {TST}; 7z a {ARX_TYPE} {OUT}/arx2', 'Everything is Ok'))
    res.append(checkout(f'cd {OUT}; 7z e arx2.{ARX_TYPE[2:]} -o{FOLDER1} -y', 'Everything is Ok'))
    for i in make_files:
        res.append(checkout(f'ls {FOLDER1}', i))
    assert all(res), 'test2 FAIL'


def test_step3(logger):
    """Проверка архива на повереждение."""
    assert checkout(f'cd {OUT}; 7z t arx2.{ARX_TYPE[2:]}', 'Everything is Ok'), 'test3 FAIL'


def test_step4(get_list_files, logger):
    """Проверка удаления архива."""
    assert checkout(f'cd {OUT}; 7z d arx2.{ARX_TYPE[2:]} {get_list_files[0]}', 'Everything is Ok'), 'test4 FAIL'


def test_step5(get_list_files, logger):
    """Проверка обновления архива."""
    assert checkout(f'cd {TST}; echo "hello" >> {get_list_files[1]}; cd {OUT};' +
                    f'7z u arx2.{ARX_TYPE[2:]} {TST}/{get_list_files[1]}', 'Everything is Ok'), 'test5 FAIL'


def test_step6(get_bad_file, logger):
    """Проверка поврежденного архива на повреждение - негативный тест."""
    assert checkout(f'cd {OUT}; 7z t arx_bad.{ARX_TYPE[2:]}', 'Open ERROR'), 'test6 FAIL'


def test_step7(get_bad_file, logger):
    """Проверка распаковки битого архива - негативный тест."""
    assert checkout(f'cd {OUT}; 7z e arx_bad.{ARX_TYPE[2:]} -o{FOLDER1} -y', 'Open ERROR'), 'test7 FAIL'

# python3 -m pytest test_task1_sem.py