import time

from selenium.webdriver.remote.webelement import WebElement

from .config import DELAY_TIME


def wait():
    """Pausa a execução pelo tempo definido no arquivo de configuração."""
    time.sleep(DELAY_TIME)


def slow_type(element: WebElement, text: str, delay: float = 0.05):
    """Digita o texto caractere por caractere com um atraso."""
    for character in text:
        element.send_keys(character)
        time.sleep(delay)
