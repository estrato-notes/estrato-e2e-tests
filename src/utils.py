import time

from .config import DELAY_TIME


def wait():
    """Pausa a execução pelo tempo definido no arquivo de configuração."""
    time.sleep(DELAY_TIME)
