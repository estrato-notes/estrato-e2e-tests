from selenium.webdriver.common.by import By

from src.config import BASE_URL
from src.utils import (
    slow_type,
    wait,
    wait_for_clickable,
    wait_for_element,
    wait_for_overlay_gone,
    wait_for_url_contains,
)


def go_to_template(driver):
    wait_for_overlay_gone(driver)
    if "/templates" not in driver.current_url:
        driver.get(f"{BASE_URL}/templates")
        wait_for_url_contains(driver, "/templates")
        wait()


def create_template_from_scratch(driver, data):
    template_data = data["templates"]["meeting_template"]
    template_name = template_data["name"]

    go_to_template(driver)

    try:
        wait_for_clickable(
            driver, (By.XPATH, "//button[contains(., 'Novo Template')]")
        ).click()
        wait(1)
    except Exception as e:
        print(f"[Templates] Erro ao clicar em 'Novo Template': {e}")
        return

    try:
        title_input = wait_for_element(
            driver, (By.XPATH, "//input[@placeholder='Título do Template']")
        )
        title_input.clear()
        title_input.send_keys(template_name)
        wait(0.5)
    except Exception as e:
        print(f"[Templates] Erro ao encontrar input de título: {e}")
        return

    try:
        content_area = wait_for_element(
            driver,
            (By.XPATH, "//textarea[@placeholder='Digite o conteúdo do template...']"),
        )
        slow_type(content_area, template_data["content"])
        wait(0.5)
    except Exception as e:
        print(f"[Templates] Erro ao preencher conteúdo: {e}")
        return

    try:
        wait_for_clickable(
            driver, (By.XPATH, "//button[contains(., 'Salvar')]")
        ).click()
        wait_for_overlay_gone(driver)
        wait(1)
        print(f"[Templates] Template '{template_name}' salvo.")
    except Exception as e:
        print(f"[Templates] Erro ao clicar em Salvar: {e}")
        return


def create_template_from_existing_note(driver, data):
    source_note_title = data["notes"]["complete_note"]["title"]
    new_template_name = data["templates"]["from_note_template"]["name"]
    notebook_name = data["notebooks"]["college"]["name"]

    wait_for_overlay_gone(driver)

    if "/notes" not in driver.current_url:
        driver.get(f"{BASE_URL}/notes")
        wait_for_url_contains(driver, "/notes")
        wait()

    try:
        notebook_btn = wait_for_clickable(
            driver,
            (
                By.XPATH,
                f"//div[contains(@class, 'hidden lg:flex')]//button[.//span[normalize-space()='{notebook_name}']]",
            ),
        )
        notebook_btn.click()
        wait(1)
    except Exception as e:
        print(f"[Templates] Erro ao selecionar caderno {notebook_name}: {e}")
        return

    try:
        wait_for_clickable(
            driver, (By.XPATH, f"//h3[text()='{source_note_title}']")
        ).click()
        wait(1)
    except Exception as e:
        print(f"[Templates] Erro ao selecionar a nota fonte: {e}")
        return

    try:
        wait_for_clickable(
            driver, (By.XPATH, "//button[contains(., 'Mais Opções')]")
        ).click()
        wait(1)
    except Exception as e:
        print(f"[Templates] Erro ao clicar em 'Mais Opções': {e}")
        return

    try:
        wait_for_clickable(
            driver, (By.XPATH, "//div[contains(text(), 'Criar Template desta Nota')]")
        ).click()
        wait(1)
    except Exception as e:
        print(f"[Templates] Erro ao clicar na opção do menu: {e}")
        return

    try:
        name_input = wait_for_element(driver, (By.ID, "template-title"))
        name_input.clear()
        name_input.send_keys(new_template_name)
        wait(0.5)

        wait_for_clickable(
            driver, (By.XPATH, "//button[contains(text(), 'Criar Template')]")
        ).click()
        wait_for_overlay_gone(driver)
        wait(1)
    except Exception as e:
        print(f"[Templates] Erro no modal de criação de template: {e}")
        return

    try:
        driver.get(f"{BASE_URL}/templates")
        wait_for_url_contains(driver, "/templates")

        wait_for_element(
            driver, (By.XPATH, f"//h3[contains(text(), '{new_template_name}')]")
        )
        print(
            f"[Templates] Sucesso: Template '{new_template_name}' criado e verificado."
        )
    except Exception as e:
        print(
            f"[Templates] Erro: Template não encontrado na lista final. Exception: {e}"
        )
