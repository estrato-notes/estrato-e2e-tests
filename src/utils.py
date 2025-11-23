import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait(seconds=2.0):
    """Pausa forçada para esperar animações de UI."""
    time.sleep(seconds)


def wait_for_overlay_gone(driver, timeout=10):
    """
    Espera que o overlay (fundo escuro do modal) desapareça antes de prosseguir.
    Essencial para evitar ElementClickInterceptedException.
    """
    try:
        overlay_xpath = (
            "//div[contains(@data-state, 'open') and contains(@class, 'fixed inset-0')]"
        )
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.XPATH, overlay_xpath))
        )
        time.sleep(0.5)
    except (TimeoutException, NoSuchElementException):
        pass


def wait_for_element(driver, locator, timeout=30):
    """Espera visibilidade e adiciona pequena pausa para estabilidade."""
    element = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )
    return element


def wait_for_clickable(driver, locator, timeout=30):
    """
    Espera o elemento ser clicável E garante que não há overlays bloqueando.
    """
    wait_for_overlay_gone(driver)

    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))

    time.sleep(0.5)
    return element


def wait_for_url_contains(driver, snippet, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(EC.url_contains(snippet))
        return True
    except TimeoutException:
        return False


def wait_for_invisibility(driver, locator, timeout=10):
    """Espera um elemento desaparecer."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
    except Exception:
        pass


def slow_type(element: WebElement, text: str, delay: float = 0.1):
    """Digita devagar. Se o elemento ficar 'stale' (velho), tenta digitar o resto."""
    try:
        for character in text:
            element.send_keys(character)
            time.sleep(delay)
    except Exception as e:
        print(f"[Utils] Erro ao digitar (pode ter perdido foco): {e}")
