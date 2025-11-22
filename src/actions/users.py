import time

from selenium.webdriver.common.by import By

from src.config import BASE_URL
from src.utils import wait


def execute_register(driver, data):
    """
    Executa o fluxo de registro de usuário.
    """
    user = data["user"]

    print(f"[Register] Iniciando registro para: {user['email']}")

    if "/register" not in driver.current_url:
        driver.get(f"{BASE_URL}/register")
        wait()

    driver.find_element(By.ID, "name").send_keys(user["full_name"])
    wait()
    driver.find_element(By.ID, "email").send_keys(user["email"])
    wait()
    driver.find_element(By.ID, "password").send_keys(user["password"])
    wait()

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait()

    time.sleep(5)

    if "/dashboard" in driver.current_url:
        print("[Register] Sucesso: Redirecionado para Dashboard.")
    else:
        print("[Register] Aviso: Não redirecionado para Dashboard (pode já existir).")


def login(driver, data):
    """
    Executa o fluxo de login.
    """
    user = data["user"]

    if "/login" not in driver.current_url and "/dashboard" not in driver.current_url:
        driver.get(f"{BASE_URL}/login")
        wait()

    if "/dashboard" in driver.current_url:
        logout(driver)

    driver.find_element(By.ID, "email").send_keys(user["email"])
    wait()
    driver.find_element(By.ID, "password").send_keys(user["password"])
    wait()

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    wait()
    time.sleep(5)


def logout(driver):
    """
    Realiza o logout através do menu do usuário no AppShell.
    """
    if "/dashboard" not in driver.current_url and "/notes" not in driver.current_url:
        driver.get(f"{BASE_URL}/dashboard")
        wait()

    avatar_btn = driver.find_element(
        By.XPATH, "//button[.//span[contains(@class, 'rounded-full')]]"
    )
    avatar_btn.click()
    wait()

    logout_btn = driver.find_element(
        By.XPATH, "//div[@role='menuitem'][contains(., 'Sair')]"
    )
    logout_btn.click()
    wait()


def login_new_password(driver, data):
    """
    Executa o fluxo de login.
    """
    user = data["user"]

    if "/login" not in driver.current_url and "/dashboard" not in driver.current_url:
        driver.get(f"{BASE_URL}/login")
        wait()

    if "/dashboard" in driver.current_url:
        logout(driver)

    driver.find_element(By.ID, "email").send_keys(user["email"])
    wait()
    driver.find_element(By.ID, "password").send_keys(user["new_password"])
    wait()

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    wait()
    time.sleep(5)
