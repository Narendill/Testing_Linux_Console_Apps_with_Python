# Доработать функцию из предыдущего задания таким образом, чтобы у неё
# появился дополнительный режим работы, в котором вывод разбивается на слова
# с удалением всех знаков пунктуации (их можно взять из списка string.punctuation модуля string).
# В этом режиме должно проверяться наличие слова в выводе.

import subprocess
import doctest
import string


def check_text(command: str, text: str, mode: bool = False) -> bool:
    """
    Выполняет команду и, если она выполнена успешно, ищет текст в её выводе.
    >>> check_text('cat /etc/os-release', 'jammy')
    True
    >>> check_text('cat /etc/os-release', 'jammy999', mode=False)
    False
    >>> check_text('ls /', 'etc')
    True
    >>> check_text('cat /etc/os-release', 'VERSION', mode=True)
    True
    >>> check_text('ls /', 'et', mode=True)
    False
    """
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    # Обычный режим (старая функция): mode = False:
    if not mode:
        if text in result.stdout and result.returncode == 0:
            return True
        else:
            return False
    # Дополнительный режим: mode = True:
    else:
        res_out = result.stdout
        for i in string.punctuation:
            if i in res_out:
                res_out = res_out.replace(i, ' ')
        res_out = res_out.split()
        if text in res_out:
            return True
        else:
            return False


if __name__ == '__main__':
    doctest.testmod(verbose=True)

