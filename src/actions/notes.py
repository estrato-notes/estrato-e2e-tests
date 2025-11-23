from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.config import BASE_URL
from src.utils import (
    slow_type,
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


def create_complete_note(driver, data):
    note_data = data["notes"]["complete_note"]
    notebook_name = data["notebooks"]["college"]["name"]

    go_to_notes(driver)

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
        print(f"[Notes] Erro ao selecionar caderno {notebook_name}: {e}")
        return

    try:
        wait_for_clickable(
            driver,
            (
                By.XPATH,
                "//div[contains(@class, 'lg:col-span-4')]//button[contains(., 'Nova Nota')]",
            ),
        ).click()
        wait(1)
    except Exception as e:
        print(f"[Notes] Erro crítico: Botão 'Nova Nota' da lista não encontrado. {e}")
        return

    title_input = wait_for_element(
        driver, (By.XPATH, "//input[contains(@class, 'text-lg font-semibold')]")
    )
    title_input.clear()
    title_input.send_keys(note_data["title"])
    wait(0.5)

    content_area = wait_for_element(
        driver, (By.XPATH, "//textarea[@placeholder='Comece a escrever aqui...']")
    )
    slow_type(content_area, note_data["content"])
    wait(0.5)

    wait_for_clickable(driver, (By.XPATH, "//button[contains(., 'Salvar')]")).click()
    wait(1)

    tag_name = note_data["tag_association"]

    try:
        tag_input = wait_for_element(
            driver, (By.XPATH, "//input[@placeholder='nova tag']")
        )
        tag_input.send_keys(tag_name)
        tag_input.send_keys(Keys.ENTER)
        wait(1)
    except Exception as e:
        print(f"[Notes] Erro ao adicionar tag: {e}")

    try:
        wait_for_clickable(
            driver, (By.XPATH, "//button[contains(., 'Visualizar')]")
        ).click()
        wait(2)
    except Exception as e:
        print(f"[Notes] Erro ao tentar visualizar a nota: {e}")

    driver.refresh()
    wait(3)


def create_note_from_template(driver, data):
    template_name = data["templates"]["meeting_template"]["name"]

    go_to_notes(driver)

    try:
        wait_for_clickable(
            driver, (By.XPATH, "//header//button[contains(., 'Nova Nota')]")
        ).click()
        wait(1)
    except Exception as e:
        print(f"[Notes] Erro ao abrir modal global: {e}")
        return

    try:
        wait_for_clickable(
            driver, (By.XPATH, "//div[contains(text(), 'Criar a partir de template')]")
        ).click()
        wait(1)
    except Exception as e:
        print(f"[Notes] Erro ao clicar na opção de template: {e}")
        return

    try:
        wait_for_clickable(
            driver, (By.XPATH, f"//button[.//h3[contains(text(), '{template_name}')]]")
        ).click()

        wait_for_overlay_gone(driver)
        wait(1)

    except Exception as e:
        print(f"[Notes] Erro ao selecionar o template na lista: {e}")
        return

    try:
        title_input = wait_for_element(
            driver, (By.XPATH, "//input[contains(@class, 'text-lg font-semibold')]")
        )
        current_title = title_input.get_attribute("value")

        if template_name in current_title:
            print(
                f"[Notes] Sucesso: Nota criada via template. Título: '{current_title}'"
            )
        else:
            print(
                f"[Notes] Aviso: Título '{current_title}' difere do template '{template_name}'."
            )

    except Exception as e:
        print(f"[Notes] Erro na validação final: {e}")


def edit_existing_note(driver, data):
    original_title = data["notes"]["complete_note"]["title"]
    new_title = data["notes"]["edit_note"]["new_title"]
    content_addition = data["notes"]["edit_note"]["new_content"]
    notebook_name = data["notebooks"]["college"]["name"]

    go_to_notes(driver)

    try:
        wait_for_clickable(
            driver,
            (
                By.XPATH,
                f"//div[contains(@class, 'hidden lg:flex')]//button[.//span[normalize-space()='{notebook_name}']]",
            ),
        ).click()
        wait(1)

        wait_for_clickable(
            driver, (By.XPATH, f"//h3[text()='{original_title}']")
        ).click()
        wait(1)
    except Exception as e:
        print(f"[Notes] Erro ao localizar a nota para edição: {e}")
        return

    try:
        title_input = wait_for_element(
            driver, (By.XPATH, "//input[contains(@class, 'text-lg font-semibold')]")
        )
        title_input.clear()
        title_input.send_keys(new_title)
        wait(0.5)
    except Exception as e:
        print(f"[Notes] Erro ao editar título: {e}")
        return

    try:
        content_area = wait_for_element(
            driver, (By.XPATH, "//textarea[@placeholder='Comece a escrever aqui...']")
        )
        slow_type(content_area, content_addition)
    except Exception as e:
        print(f"[Notes] Erro ao editar conteúdo: {e}")
        return

    try:
        wait_for_clickable(
            driver, (By.XPATH, "//button[contains(., 'Salvar')]")
        ).click()
        wait(1)
    except Exception as e:
        print(f"[Notes] Erro ao salvar: {e}")
        return


def move_note(driver, data):
    note_title = data["notes"]["edit_note"]["new_title"]
    source_notebook = data["notebooks"]["college"]["name"]
    target_notebook = data["notebooks"]["projects"]["new_name"]

    go_to_notes(driver)

    try:
        wait_for_clickable(
            driver,
            (
                By.XPATH,
                f"//div[contains(@class, 'hidden lg:flex')]//button[.//span[normalize-space()='{source_notebook}']]",
            ),
        ).click()
        wait(1)
    except Exception as e:
        print(f"[Notes] Erro ao acessar caderno de origem: {e}")
        return

    try:
        wait_for_clickable(
            driver, (By.XPATH, f"//div[h3[text()='{note_title}']]//button")
        ).click()
        wait(0.5)
    except Exception as e:
        print(f"[Notes] Erro ao clicar no menu da nota: {e}")
        return

    try:
        wait_for_clickable(
            driver, (By.XPATH, "//div[@role='menuitem'][contains(., 'Mover para...')]")
        ).click()
        wait(0.5)

        wait_for_clickable(
            driver,
            (By.XPATH, f"//div[@role='menuitem'][contains(., '{target_notebook}')]"),
        ).click()

        wait_for_overlay_gone(driver)
        wait(1)

    except Exception as e:
        print(f"[Notes] Erro ao selecionar destino no menu: {e}")
        return


def favorite_note(driver, data):
    note_title = data["notes"]["edit_note"]["new_title"]
    notebook_name = data["notebooks"]["projects"]["new_name"]

    go_to_notes(driver)

    try:
        wait_for_clickable(
            driver,
            (
                By.XPATH,
                f"//div[contains(@class, 'hidden lg:flex')]//button[.//span[normalize-space()='{notebook_name}']]",
            ),
        ).click()
        wait(1)
    except Exception as e:
        print(f"[Notes] Erro ao acessar caderno: {e}")
        return

    try:
        wait_for_clickable(
            driver,
            (
                By.XPATH,
                f"//h3[contains(text(), '{note_title}')]/ancestor::div[contains(@class, 'cursor-pointer')]/preceding-sibling::button",
            ),
        ).click()
        wait(1)
    except Exception as e:
        print(f"[Notes] Erro ao clicar na estrela de favorito: {e}")


def delete_draft_note(driver, data):
    note_data = data["notes"]["delete_note"]

    go_to_notes(driver)

    try:
        wait_for_clickable(
            driver, (By.XPATH, "//button[contains(., 'Nova Nota')]")
        ).click()
        wait(0.5)

        wait_for_clickable(
            driver, (By.XPATH, "//div[contains(text(), 'Criar nota do zero')]")
        ).click()
        wait(3)

        title_input = wait_for_element(
            driver, (By.XPATH, "//input[contains(@class, 'text-lg font-semibold')]")
        )
        title_input.clear()
        title_input.send_keys(note_data["title"])
        wait(0.5)

        content_area = wait_for_element(
            driver, (By.XPATH, "//textarea[@placeholder='Comece a escrever aqui...']")
        )
        slow_type(content_area, note_data["content"])

        wait_for_clickable(
            driver, (By.XPATH, "//button[contains(., 'Salvar')]")
        ).click()
        wait(2)
    except Exception as e:
        print(f"[Notes] Erro na preparação (criação da nota): {e}")
        return

    try:
        wait_for_clickable(
            driver, (By.XPATH, f"//div[h3[text()='{note_data['title']}']]//button")
        ).click()
        wait(0.5)

        wait_for_clickable(
            driver, (By.XPATH, "//div[@role='menuitem'][contains(., 'Apagar Nota')]")
        ).click()
        wait(1)

        wait_for_clickable(
            driver,
            (
                By.XPATH,
                "//button[contains(@class, 'bg-destructive') and contains(., 'Apagar')]",
            ),
        ).click()

        wait_for_overlay_gone(driver)
        wait(1)

    except Exception as e:
        print(f"[Notes] Erro durante a exclusão: {e}")
