from selenium.webdriver.common.by import By

from src.config import BASE_URL
from src.utils import (
    wait,
    wait_for_clickable,
    wait_for_element,
    wait_for_overlay_gone,
    wait_for_url_contains,
)


def go_to_notes(driver):
    wait_for_overlay_gone(driver)
    if "/notes" not in driver.current_url:
        driver.get(f"{BASE_URL}/notes")
        wait_for_url_contains(driver, "/notes")
        wait()


def get_notebook_row(driver, notebook_name):
    notebook_xpath = (
        f"//div[contains(@class, 'hidden lg:flex')]"
        f"//div[contains(@class, 'flex') and contains(@class, 'gap-2')]"
        f"[.//span[normalize-space()='{notebook_name}']] "
    )
    return wait_for_element(driver, (By.XPATH, notebook_xpath))


def open_notebook_menu(driver, notebook_name):
    # Garante que a linha está visível
    notebook_row = get_notebook_row(driver, notebook_name)

    # Encontra o botão dentro da linha (último botão geralmente é o menu)
    menu_btn = notebook_row.find_element(By.XPATH, ".//button[last()]")

    # Pausa breve para garantir interatividade
    wait(0.5)
    menu_btn.click()
    wait(1)  # Espera o menu abrir


def create_notebook(driver, notebook_name):
    go_to_notes(driver)

    wait_for_clickable(
        driver, (By.XPATH, "//button[contains(., 'Novo Caderno')]")
    ).click()
    wait(1)  # Espera modal abrir

    name_input = wait_for_element(driver, (By.ID, "notebook-name"))
    name_input.clear()
    name_input.send_keys(notebook_name)
    wait(0.5)

    driver.find_element(By.XPATH, "//button[contains(text(), 'Criar')]").click()

    wait_for_overlay_gone(driver)  # Espera modal fechar
    print(f"[Notebooks] Caderno '{notebook_name}' criado.")


def rename_notebook(driver, old_name, new_name):
    go_to_notes(driver)

    try:
        open_notebook_menu(driver, old_name)

        wait_for_clickable(
            driver, (By.XPATH, "//div[@role='menuitem'][contains(., 'Renomear')]")
        ).click()
        wait(1)  # Espera modal abrir

        rename_input = wait_for_element(driver, (By.ID, "rename-notebook"))
        rename_input.clear()
        rename_input.send_keys(new_name)
        wait(0.5)

        driver.find_element(By.XPATH, "//button[contains(text(), 'Renomear')]").click()

        wait_for_overlay_gone(driver)  # Espera modal fechar

    except Exception as e:
        print(f"[Notebooks] Erro ao renomear: {e}")


def toggle_favorite_notebook(driver, notebook_name):
    go_to_notes(driver)

    try:
        notebook_row = get_notebook_row(driver, notebook_name)
        star_btn = notebook_row.find_element(By.XPATH, ".//button[1]")
        star_btn.click()
        wait(1)  # Espera atualização da UI
    except Exception as e:
        print(f"[Notebooks] Erro ao favoritar: {e}")


def delete_notebook(driver, notebook_name):
    go_to_notes(driver)

    try:
        open_notebook_menu(driver, notebook_name)

        wait_for_clickable(
            driver, (By.XPATH, "//div[@role='menuitem'][contains(., 'Apagar Caderno')]")
        ).click()
        wait(1)  # Espera modal de confirmação

        wait_for_clickable(
            driver,
            (
                By.XPATH,
                "//button[contains(@class, 'bg-destructive') and contains(., 'Apagar')]",
            ),
        ).click()

        wait_for_overlay_gone(driver)  # Espera modal fechar e item sumir

    except Exception as e:
        print(f"[Notebooks] Erro ao excluir: {e}")


def execute_notebook_flow(driver, data):
    notebooks = data["notebooks"]

    for notebook_data in notebooks.values():
        create_notebook(driver, notebook_data["name"])

        if notebook_data.get("should_favorite"):
            toggle_favorite_notebook(driver, notebook_data["name"])

    rename_notebook(
        driver, notebooks["projects"]["name"], notebooks["projects"]["new_name"]
    )

    delete_notebook(driver, notebooks["deletion"]["name"])
