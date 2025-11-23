from selenium.webdriver.common.by import By

from src.utils import (
    slow_type,
    wait,
    wait_for_clickable,
    wait_for_element,
    wait_for_overlay_gone,
    wait_for_url_contains,
)


def go_to_profile(driver):
    wait_for_overlay_gone(driver)

    wait_for_clickable(
        driver, (By.XPATH, "//button[.//span[contains(@class, 'rounded-full')]]")
    ).click()
    wait(0.5)

    wait_for_clickable(
        driver, (By.XPATH, "//div[@role='menuitem'][contains(., 'Meu Perfil')]")
    ).click()

    wait_for_url_contains(driver, "/profile")
    wait(2)


def update_name(driver, data):
    new_name = data["user"]["new_full_name"]

    go_to_profile(driver)

    try:
        wait_for_clickable(
            driver, (By.XPATH, "//button[contains(text(), 'Alterar')]")
        ).click()
        wait(1)

        name_input = wait_for_element(driver, (By.ID, "name"))
        name_input.clear()
        slow_type(name_input, new_name)
        wait(0.5)

        wait_for_clickable(
            driver, (By.XPATH, "//button[contains(text(), 'Salvar')]")
        ).click()
        wait(2)  # Espera salvar

    except Exception as e:
        print(f"[Profile] Erro ao atualizar nome: {e}")


def change_password(driver, data):
    current_password = data["user"]["password"]
    new_password = data["user"]["new_password"]

    go_to_profile(driver)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    wait(1)

    try:
        xpath_btn = "//h3[contains(text(), 'Alterar Senha')]/ancestor::div[contains(@class, 'justify-between')]//button"

        wait_for_clickable(driver, (By.XPATH, xpath_btn)).click()
        wait(1)

        current_input = wait_for_element(driver, (By.ID, "current-password"))
        current_input.send_keys(current_password)

        driver.find_element(By.ID, "new-password").send_keys(new_password)
        driver.find_element(By.ID, "confirm-password").send_keys(new_password)
        wait(1)

        wait_for_clickable(
            driver, (By.XPATH, "//button[contains(text(), 'Alterar Senha')]")
        ).click()
        wait(2)

    except Exception as e:
        print(f"[Profile] Erro ao alterar senha: {e}")


def delete_account(driver):
    go_to_profile(driver)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    wait(1)

    try:
        wait_for_clickable(
            driver,
            (
                By.XPATH,
                "//button[contains(@class, 'bg-destructive') and contains(text(), 'Apagar')]",
            ),
        ).click()
        wait(1)

        wait_for_clickable(
            driver,
            (
                By.XPATH,
                "//button[contains(@class, 'bg-destructive') and contains(text(), 'Excluir Conta')]",
            ),
        ).click()

        wait_for_overlay_gone(driver)
        wait_for_url_contains(driver, "/login")
        wait(2)

    except Exception as e:
        print(f"[Profile] Erro ao excluir conta: {e}")
