# Задание 1.
# Дополнить проект тестами, проверяющими команды вывода списка файлов (l) и разархивирования с путями (x).
#
# Задание 2.
# Установить пакет для расчёта crc32
# sudo apt install libarchive-zip-perl
# Доработать проект, добавив тест команды расчёта хеша (h). Проверить, что хеш совпадает с рассчитанным командой crc32.

import subprocess

TST = '/home/user/tst'
OUT = '/home/user/out'
FOLDER1 = '/home/user/folder1'


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            encoding='utf-8')
    if text in result.stdout and result.returncode == 0 or text in result.stderr:
        return True
    else:
        return False


def test_step1():
    """Проверка на создание архива."""
    res1 = checkout(f'cd {TST}; 7z a ../out/arx2', 'Everything is Ok')
    res2 = checkout(f'ls {OUT}', 'arx2.7z')
    assert res1 and res2, 'test1 FAIL'


def test_step2():
    """Проверка списка файлов в архиве и спика файлов, которые должны были заархивироваться."""
    file_list = subprocess.run(f'cd {TST}; ls', shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    file_list = file_list.stdout.split('\n')[:-1]  # Тут хранится список файлов, которые должны были архивироваться

    # Циклом проверяем наличие каждого файла в выводе флага 'l':
    for file in file_list:
        assert checkout(f'cd {OUT}; 7z l arx2.7z', f'{file}'), f'test2 FAIL: file \'{file}\' is not in archive'


def test_step_3():
    """Проверка разархивации с полным путём."""
    # Рекурсивно посмотрели весь каталог с иходниками:
    res1 = subprocess.run(f'cd {TST}; ls -R', shell=True, stdout=subprocess.PIPE, encoding='utf-8')

    # Распаковка архива в FOLDER1 с флагом 'x':
    res2 = checkout(f'cd {OUT}; 7z x arx2.7z -o{FOLDER1} -y', 'Everything is Ok')

    # Рекурсивно посмотрели что распаковалось:
    res3 = subprocess.run(f'cd {FOLDER1}; ls -R', shell=True, stdout=subprocess.PIPE, encoding='utf-8')

    assert res1.stdout == res3.stdout and res2, 'test3 FAIL'


def test_step_4():
    """Проверка хэша архива."""
    # Тут храним хэш от crc32:
    res1 = subprocess.run(f'cd {OUT}; crc32 arx2.7z', shell=True, stdout=subprocess.PIPE, encoding='utf-8')

    # Ищем хэш от crc32 в выводе хэша от 7z отдельно в нижнем и верхнем регистре:
    res_lower = checkout(f'cd {OUT}; 7z h arx2.7z', f'{res1.stdout.lower()}')
    res_upper = checkout(f'cd {OUT}; 7z h arx2.7z', f'{res1.stdout.upper()}')

    assert res_upper or res_lower, 'test4 FAIL'
