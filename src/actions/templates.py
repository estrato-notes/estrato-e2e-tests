from selenium.webdriver.common.by import By

from src.config import BASE_URL
from src.utils import slow_type, wait


def go_to_template(driver):
    if "/templates" not in driver.current_url:
        driver.get(f"{BASE_URL}/templates")
        wait()


def create_template_from_scratch(driver, data):
    template_data = data["templates"]["meeting_template"]
    template_name = template_data["name"]

    go_to_template(driver)

    try:
        driver.find_element(By.XPATH, "//button[contains(., 'Novo Template')]").click()
        wait()
    except Exception as e:
        print(f"[Templates] Erro ao clicar em 'Novo Template': {e}")
        return

    try:
        title_input = driver.find_element(
            By.XPATH, "//input[@placeholder='Título do Template']"
        )
        title_input.clear()
        title_input.send_keys(template_name)
        wait()
    except Exception as e:
        print(f"[Templates] Erro ao encontrar input de título: {e}")
        return

    try:
        content_area = driver.find_element(
            By.XPATH, "//textarea[@placeholder='Digite o conteúdo do template...']"
        )
        slow_type(content_area, template_data["content"])
        wait()
    except Exception as e:
        print(f"[Templates] Erro ao preencher conteúdo: {e}")
        return

    try:
        driver.find_element(By.XPATH, "//button[contains(., 'Salvar')]").click()
        wait()
    except Exception as e:
        print(f"[Templates] Erro ao clicar em Salvar: {e}")
        return


def create_template_from_existing_note(driver, data):
    source_note_title = data["notes"]["complete_note"]["title"]
    new_template_name = data["templates"]["from_note_template"]["name"]
    notebook_name = data["notebooks"]["college"]["name"]

    if "/notes" not in driver.current_url:
        driver.get(f"{BASE_URL}/notes")
        wait()

    try:
        notebook_btn = driver.find_element(
            By.XPATH,
            f"//div[contains(@class, 'hidden lg:flex')]//button[.//span[normalize-space()='{notebook_name}']]",
        )
        notebook_btn.click()
        wait()
    except Exception as e:
        print(f"[Templates] Erro ao selecionar caderno {notebook_name}: {e}")
        return

    try:
        driver.find_element(By.XPATH, f"//h3[text()='{source_note_title}']").click()
        wait()
    except Exception as e:
        print(f"[Templates] Erro ao selecionar a nota fonte: {e}")
        return

    try:
        driver.find_element(By.XPATH, "//button[contains(., 'Mais Opções')]").click()
        wait()
    except Exception as e:
        print(f"[Templates] Erro ao clicar em 'Mais Opções': {e}")
        return

    try:
        driver.find_element(
            By.XPATH, "//div[contains(text(), 'Criar Template desta Nota')]"
        ).click()
        wait()
    except Exception as e:
        print(f"[Templates] Erro ao clicar na opção do menu: {e}")
        return

    try:
        name_input = driver.find_element(By.ID, "template-title")
        name_input.clear()
        name_input.send_keys(new_template_name)
        wait()

        driver.find_element(
            By.XPATH, "//button[contains(text(), 'Criar Template')]"
        ).click()
        wait()
    except Exception as e:
        print(f"[Templates] Erro no modal de criação de template: {e}")
        return

    try:
        driver.get(f"{BASE_URL}/templates")
        wait()

        driver.find_element(By.XPATH, f"//h3[contains(text(), '{new_template_name}')]")
        print(
            f"[Templates] Sucesso: Template '{new_template_name}' criado e verificado."
        )
    except Exception as e:
        print(
            f"[Templates] Erro: Template não encontrado na lista final. Exception: {e}"
        )
