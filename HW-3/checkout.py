import subprocess


def checkout(cmd: str, text: str) -> bool:
    """Выполняет команду и в выводе ищет текст."""
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            encoding='utf-8')
    if text in result.stdout and result.returncode == 0 or text in result.stderr:
        return True
    else:
        return False


def getout(cmd: str) -> tuple:
    """Возвращает результат выполнения команды."""
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            encoding='utf-8')
    return result.stdout.strip().split('\n'), result.stderr
