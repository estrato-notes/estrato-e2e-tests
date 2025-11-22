import time

from selenium.webdriver.common.by import By

from src.config import BASE_URL
from src.utils import wait


def go_to_notes(driver):
    if "/notes" not in driver.current_url:
        driver.get(f"{BASE_URL}/notes")
        wait()
        time.sleep(3)


def get_notebook_row(driver, notebook_name):
    notebook_xpath = (
        f"//div[contains(@class, 'hidden lg:flex')]"
        f"//div[contains(@class, 'flex') and contains(@class, 'gap-2')]"
        f"[.//span[normalize-space()='{notebook_name}']] "
    )
    return driver.find_element(By.XPATH, notebook_xpath)


def open_notebook_menu(driver, notebook_name):
    notebook_row = get_notebook_row(driver, notebook_name)

    menu_btn = notebook_row.find_element(By.XPATH, ".//button[last()]")
    menu_btn.click()
    wait()


def create_notebook(driver, notebook_name):
    wait()
    go_to_notes(driver)

    driver.find_element(By.XPATH, "//button[contains(., 'Novo Caderno')]").click()
    wait()

    name_input = driver.find_element(By.ID, "notebook-name")
    name_input.clear()
    name_input.send_keys(notebook_name)
    wait()

    driver.find_element(By.XPATH, "//button[contains(text(), 'Criar')]").click()
    wait()


def rename_notebook(driver, old_name, new_name):
    go_to_notes(driver)

    try:
        open_notebook_menu(driver, old_name)

        driver.find_element(
            By.XPATH, "//div[@role='menuitem'][contains(., 'Renomear')]"
        ).click()
        wait()

        rename_input = driver.find_element(By.ID, "rename-notebook")
        rename_input.clear()
        rename_input.send_keys(new_name)
        wait()

        driver.find_element(By.XPATH, "//button[contains(text(), 'Renomear')]").click()
        wait()

    except Exception as e:
        print(f"[Notebooks] Erro ao renomear: {e}")


def toggle_favorite_notebook(driver, notebook_name):
    go_to_notes(driver)

    try:
        notebook_row = get_notebook_row(driver, notebook_name)

        star_btn = notebook_row.find_element(By.XPATH, ".//button[1]")
        star_btn.click()
        wait()

    except Exception as e:
        print(f"[Notebooks] Erro ao favoritar: {e}")


def delete_notebook(driver, notebook_name):
    go_to_notes(driver)

    try:
        open_notebook_menu(driver, notebook_name)

        driver.find_element(
            By.XPATH, "//div[@role='menuitem'][contains(., 'Apagar Caderno')]"
        ).click()
        wait()

        confirm_btn = driver.find_element(
            By.XPATH,
            "//button[contains(@class, 'bg-destructive') and contains(., 'Apagar')]",
        )
        confirm_btn.click()
        wait()

    except Exception as e:
        print(f"[Notebooks] Erro ao excluir: {e}")


def execute_notebook_flow(driver, data):
    notebooks = data["notebooks"]

    for notebook_data in notebooks.values():
        create_notebook(driver, notebook_data["name"])
        wait()

        if notebook_data.get("should_favorite"):
            toggle_favorite_notebook(driver, notebook_data["name"])

    rename_notebook(
        driver, notebooks["projects"]["name"], notebooks["projects"]["new_name"]
    )

    delete_notebook(driver, notebooks["deletion"]["name"])
