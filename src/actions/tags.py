from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.config import BASE_URL
from src.utils import (
    wait,
    wait_for_clickable,
    wait_for_element,
    wait_for_overlay_gone,
    wait_for_url_contains,
)


def go_to_tags(driver):
    wait_for_overlay_gone(driver)
    if "/tags" not in driver.current_url:
        driver.get(f"{BASE_URL}/tags")
        wait_for_url_contains(driver, "/tags")
        wait()


def add_tags_to_active_note(driver, data):
    driver.refresh()
    wait(2)

    note_title = data["notes"]["edit_note"]["new_title"]
    tag_name = data["tags"]["study"]["name"]

    if "/notes" not in driver.current_url:
        driver.get(f"{BASE_URL}/notes")
        wait_for_url_contains(driver, "/notes")
        wait()

    try:
        wait_for_clickable(driver, (By.XPATH, f"//h3[text()='{note_title}']")).click()
        wait(1)

        tag_input = wait_for_element(
            driver, (By.XPATH, "//input[@placeholder='nova tag']")
        )
        tag_input.send_keys(tag_name)
        tag_input.send_keys(Keys.ENTER)
        wait(1)

        wait_for_element(driver, (By.XPATH, f"//span[contains(text(), '{tag_name}')]"))

        driver.refresh()
        wait(2)
    except Exception as e:
        print(f"[Tags] Erro ao adicionar tag na nota: {e}")


def create_tag_via_dedicated_page(driver, data):
    tag_name = data["tags"]["deletion"]["name"]
    go_to_tags(driver)

    try:
        input_elem = wait_for_element(driver, (By.ID, "new-tag"))
        input_elem.clear()
        input_elem.send_keys(tag_name)
        wait(0.5)

        wait_for_clickable(
            driver, (By.XPATH, "//button[contains(., 'Criar Tag')]")
        ).click()
        wait(1)

        wait_for_element(driver, (By.XPATH, f"//span[normalize-space()='{tag_name}']"))
    except Exception as e:
        print(f"[Tags] Erro ao criar tag na página dedicada: {e}")


def rename_tag(driver, data):
    old_name = data["tags"]["urgent"]["name"]
    new_name = data["tags"]["urgent"]["new_name"]
    go_to_tags(driver)

    try:
        tag_row_xpath = f"//div[contains(@class, 'rounded-lg') and .//span[contains(text(), '{old_name}')]]"

        wait_for_clickable(
            driver, (By.XPATH, f"{tag_row_xpath}//button[contains(., 'Editar')]")
        ).click()
        wait(1)

        input_elem = wait_for_element(driver, (By.ID, "edit-tag"))
        input_elem.clear()
        input_elem.send_keys(new_name)
        wait(0.5)

        wait_for_clickable(
            driver, (By.XPATH, "//button[contains(., 'Salvar')]")
        ).click()
        wait_for_overlay_gone(driver)
        wait(1)
    except Exception as e:
        print(f"[Tags] Erro ao renomear tag: {e}")


def delete_tag(driver, data):
    tag_name = data["tags"]["deletion"]["name"]
    go_to_tags(driver)

    try:
        tag_row_xpath = f"//div[contains(@class, 'rounded-lg') and .//span[normalize-space()='{tag_name}']]"

        wait_for_clickable(
            driver, (By.XPATH, f"{tag_row_xpath}//button[contains(., 'Apagar')]")
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
        print(f"[Tags] Erro ao tentar excluir a tag: {e}")
