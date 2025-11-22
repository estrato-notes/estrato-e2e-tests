import time

from selenium.webdriver.common.by import By

from src.utils import slow_type, wait


def go_to_profile(driver):
    driver.find_element(
        By.XPATH, "//button[.//span[contains(@class, 'rounded-full')]]"
    ).click()
    wait()

    driver.find_element(
        By.XPATH, "//div[@role='menuitem'][contains(., 'Meu Perfil')]"
    ).click()
    wait()
    time.sleep(3)


def update_name(driver, data):
    new_name = data["user"]["new_full_name"]

    go_to_profile(driver)

    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Alterar')]").click()
        wait()

        name_input = driver.find_element(By.ID, "name")
        name_input.clear()
        slow_type(name_input, new_name)
        wait()

        driver.find_element(By.XPATH, "//button[contains(text(), 'Salvar')]").click()
        wait()
    except Exception as e:
        print(f"[Profile] Erro ao atualizar nome: {e}")


def change_password(driver, data):
    current_password = data["user"]["password"]
    new_password = data["user"]["new_password"]

    go_to_profile(driver)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    wait()

    try:
        xpath_btn = "//h3[contains(text(), 'Alterar Senha')]/ancestor::div[contains(@class, 'justify-between')]//button"

        driver.find_element(By.XPATH, xpath_btn).click()
        wait()

        driver.find_element(By.ID, "current-password").send_keys(current_password)
        wait()
        driver.find_element(By.ID, "new-password").send_keys(new_password)
        wait()
        driver.find_element(By.ID, "confirm-password").send_keys(new_password)
        wait()

        driver.find_element(
            By.XPATH, "//button[contains(text(), 'Alterar Senha')]"
        ).click()
        wait()
    except Exception as e:
        print(f"[Profile] Erro ao alterar senha: {e}")


def delete_account(driver):
    go_to_profile(driver)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    wait()

    try:
        driver.find_element(
            By.XPATH,
            "//button[contains(@class, 'bg-destructive') and contains(text(), 'Apagar')]",
        ).click()
        wait()

        driver.find_element(
            By.XPATH,
            "//button[contains(@class, 'bg-destructive') and contains(text(), 'Excluir Conta')]",
        ).click()
        wait()
        time.sleep(2)
    except Exception as e:
        print(f"[Profile] Erro ao excluir conta: {e}")
