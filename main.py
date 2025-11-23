import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.actions import (
    dashboard,
    notebooks,
    notes,
    profile,
    search,
    tags,
    templates,
    users,
)
from src.config import BASE_URL


def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


def load_json_data():
    try:
        with open("data/roteiro.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erro: Arquivo roteiro.json não encontrado.")
        exit(1)


if __name__ == "__main__":
    driver = setup_driver()
    data = load_json_data()

    try:
        print(f"Aguardando servidor responder em {BASE_URL}...")
        driver.get(BASE_URL)

        driver.delete_all_cookies()
        driver.refresh()

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("Servidor ativo. Iniciando testes...")
        time.sleep(2)

        # --- Início do Fluxo ---
        users.execute_register(driver, data)
        time.sleep(2)

        users.logout(driver)
        time.sleep(2)

        users.login(driver, data)
        time.sleep(2)

        dashboard.create_quick_note(driver, data)
        time.sleep(2)

        notebooks.execute_notebook_flow(driver, data)
        time.sleep(2)

        notes.create_complete_note(driver, data)
        time.sleep(2)

        templates.create_template_from_scratch(driver, data)
        time.sleep(2)

        notes.create_note_from_template(driver, data)
        time.sleep(2)

        templates.create_template_from_existing_note(driver, data)
        time.sleep(2)

        notes.edit_existing_note(driver, data)
        time.sleep(2)

        notes.move_note(driver, data)
        time.sleep(2)

        notes.favorite_note(driver, data)
        time.sleep(2)

        dashboard.verify_dashboard(driver)
        time.sleep(2)

        notes.delete_draft_note(driver, data)
        time.sleep(2)

        tags.add_tags_to_active_note(driver, data)
        time.sleep(2)

        tags.create_tag_via_dedicated_page(driver, data)
        time.sleep(2)

        tags.rename_tag(driver, data)
        time.sleep(2)

        dashboard.verify_dashboard(driver)
        time.sleep(2)

        tags.delete_tag(driver, data)
        time.sleep(2)

        dashboard.verify_dashboard(driver)
        time.sleep(2)

        search.perform_global_search(driver, data)
        time.sleep(2)

        dashboard.go_to_dashboard(driver)
        time.sleep(2)

        profile.update_name(driver, data)
        time.sleep(2)

        profile.change_password(driver, data)
        time.sleep(2)

        users.logout(driver)
        time.sleep(2)

        users.login_new_password(driver, data)
        time.sleep(2)

        profile.delete_account(driver)

    except Exception as e:
        print(f"Erro Crítico na execução: {e}")
    finally:
        driver.quit()
