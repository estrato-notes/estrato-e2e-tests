from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from src.config import BASE_URL
from src.utils import (
    wait,
    wait_for_clickable,
    wait_for_element,
    wait_for_overlay_gone,
    wait_for_url_contains,
)


def execute_register(driver, data):
    user = data["user"]

    print(f"[Register] Iniciando registro para: {user['email']}")

    wait_for_overlay_gone(driver)
    if "/register" not in driver.current_url:
        driver.get(f"{BASE_URL}/register")
        wait_for_url_contains(driver, "/register")
        wait(1)

    name_input = wait_for_element(driver, (By.ID, "name"))
    name_input.send_keys(user["full_name"])

    driver.find_element(By.ID, "email").send_keys(user["email"])
    driver.find_element(By.ID, "password").send_keys(user["password"])
    wait(0.5)

    wait_for_clickable(driver, (By.CSS_SELECTOR, "button[type='submit']")).click()

    # Tenta esperar o redirecionamento
    if wait_for_url_contains(driver, "/dashboard", timeout=10):
        print("[Register] Sucesso: Redirecionado para Dashboard.")
    else:
        print(
            "[Register] Aviso: Não redirecionado para Dashboard (usuário pode já existir)."
        )

    wait(1)


def logout(driver):
    """
    Realiza logout de forma segura.
    """
    wait_for_overlay_gone(driver)

    # Se não estiver no dashboard, tenta ir pra lá
    if "/dashboard" not in driver.current_url:
        driver.get(f"{BASE_URL}/dashboard")

        # Espera inteligente: ou carrega o dashboard ou cai no login (se token expirou/inválido)
        try:
            WebDriverWait(driver, 10).until(
                lambda d: "/dashboard" in d.current_url or "/login" in d.current_url
            )
        except TimeoutException:
            print(
                "[Logout] Timeout esperando carregamento inicial. Forçando ida ao login."
            )
            driver.get(f"{BASE_URL}/login")
            return

    # Se a aplicação nos jogou para o login, já estamos deslogados
    if "/login" in driver.current_url:
        return

    # Se estamos no dashboard, fazemos o logout manual
    try:
        avatar_btn = wait_for_clickable(
            driver, (By.XPATH, "//button[.//span[contains(@class, 'rounded-full')]]")
        )
        avatar_btn.click()
        wait(0.5)

        logout_btn = wait_for_clickable(
            driver, (By.XPATH, "//div[@role='menuitem'][contains(., 'Sair')]")
        )
        logout_btn.click()

        wait_for_url_contains(driver, "/login")
        wait(1)
    except Exception as e:
        print(f"[Logout] Erro ao tentar clicar em sair: {e}")
        # Fallback
        if "/login" not in driver.current_url:
            driver.get(f"{BASE_URL}/login")


def login(driver, data):
    user = data["user"]

    wait_for_overlay_gone(driver)
    if "/login" not in driver.current_url:
        driver.get(f"{BASE_URL}/login")
        wait_for_url_contains(driver, "/login")
        wait(1)

    # Se por acaso estivermos logados, faz logout
    if "/dashboard" in driver.current_url:
        logout(driver)

    email_input = wait_for_element(driver, (By.ID, "email"))
    email_input.clear()
    email_input.send_keys(user["email"])

    driver.find_element(By.ID, "password").send_keys(user["password"])
    wait(0.5)

    wait_for_clickable(driver, (By.CSS_SELECTOR, "button[type='submit']")).click()

    # Timeout maior (60s) para o Cold Start do servidor
    wait_for_url_contains(driver, "/dashboard", timeout=60)
    wait(2)


def login_new_password(driver, data):
    user = data["user"]

    wait_for_overlay_gone(driver)
    if "/login" not in driver.current_url:
        driver.get(f"{BASE_URL}/login")
        wait_for_url_contains(driver, "/login")
        wait(1)

    if "/dashboard" in driver.current_url:
        logout(driver)

    email_input = wait_for_element(driver, (By.ID, "email"))
    email_input.clear()
    email_input.send_keys(user["email"])

    driver.find_element(By.ID, "password").send_keys(user["new_password"])
    wait(0.5)

    wait_for_clickable(driver, (By.CSS_SELECTOR, "button[type='submit']")).click()

    wait_for_url_contains(driver, "/dashboard", timeout=60)
    wait(2)
