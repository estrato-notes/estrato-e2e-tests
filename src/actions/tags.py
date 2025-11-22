import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.config import BASE_URL
from src.utils import wait


def go_to_tags(driver):
    if "/tags" not in driver.current_url:
        driver.get(f"{BASE_URL}/tags")
        wait()
        time.sleep(3)


def add_tags_to_active_note(driver, data):
    driver.refresh()
    wait()

    note_title = data["notes"]["edit_note"]["new_title"]
    tag_name = data["tags"]["study"]["name"]

    if "/notes" not in driver.current_url:
        driver.get(f"{BASE_URL}/notes")
        wait()

    try:
        driver.find_element(By.XPATH, f"//h3[text()='{note_title}']").click()
        wait()

        tag_input = driver.find_element(By.XPATH, "//input[@placeholder='nova tag']")
        tag_input.send_keys(tag_name)
        tag_input.send_keys(Keys.ENTER)
        wait()

        driver.refresh()
        wait()
    except Exception as e:
        print(f"[Tags] Erro ao adicionar tag na nota: {e}")
        return


def create_tag_via_dedicated_page(driver, data):
    tag_name = data["tags"]["deletion"]["name"]

    go_to_tags(driver)

    try:
        input_elem = driver.find_element(By.ID, "new-tag")
        input_elem.clear()
        input_elem.send_keys(tag_name)
        wait()

        driver.find_element(By.XPATH, "//button[contains(., 'Criar Tag')]").click()
        wait()
    except Exception as e:
        print(f"[Tags] Erro ao criar tag na página dedicada: {e}")


def rename_tag(driver, data):
    old_name = data["tags"]["urgent"]["name"]
    new_name = data["tags"]["urgent"]["new_name"]

    go_to_tags(driver)

    try:
        tag_row_xpath = f"//div[contains(@class, 'rounded-lg') and .//span[contains(text(), '{old_name}')]]"
        driver.find_element(
            By.XPATH, f"{tag_row_xpath}//button[contains(., 'Editar')]"
        ).click()
        wait()

        input_elem = driver.find_element(By.ID, "edit-tag")
        input_elem.clear()
        input_elem.send_keys(new_name)
        wait()

        driver.find_element(By.XPATH, "//button[contains(., 'Salvar')]").click()
        wait()
    except Exception as e:
        print(f"[Tags] Erro ao renomear tag: {e}")


def delete_tag(driver, data):
    tag_name = data["tags"]["deletion"]["name"]

    go_to_tags(driver)

    try:
        tag_row_xpath = f"//div[contains(@class, 'rounded-lg') and .//span[normalize-space()='{tag_name}']]"
        driver.find_element(
            By.XPATH, f"{tag_row_xpath}//button[contains(., 'Apagar')]"
        ).click()
        wait()

        driver.find_element(
            By.XPATH,
            "//button[contains(@class, 'bg-destructive') and contains(., 'Apagar')]",
        ).click()
        wait()
    except Exception as e:
        print(f"[Tags] Erro ao tentar excluir a tag: {e}")
