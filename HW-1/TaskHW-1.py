# Написать функцию на Python, которой передаются в качестве параметров команда и текст.
# Функция должна возвращать True, если команда успешно выполнена и текст найден в её
# выводе и False в противном случае.
# Передаваться должна только одна строка, разбиение вывода использовать не нужно.

import subprocess
import doctest


def check_text(command: str, text: str) -> bool:
    """
    Выполняет команду и, если она выполнена успешно, ищет текст в её выводе.
    >>> check_text('cat /etc/os-release', 'jammy')
    True
    >>> check_text('cat /etc/os-release', 'jammy999')
    False
    >>> check_text('ls /', 'etc')
    True
    """
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')

    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    doctest.testmod(verbose=True)

