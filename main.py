import json
import time

from selenium import webdriver

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
        users.execute_register(driver, data)
        users.logout(driver)
        users.login(driver, data)
        dashboard.create_quick_note(driver, data)
        notebooks.execute_notebook_flow(driver, data)
        notes.create_complete_note(driver, data)
        templates.create_template_from_scratch(driver, data)
        notes.create_note_from_template(driver, data)
        templates.create_template_from_existing_note(driver, data)
        notes.edit_existing_note(driver, data)
        notes.move_note(driver, data)
        notes.favorite_note(driver, data)
        dashboard.verify_dashboard(driver)
        notes.delete_draft_note(driver, data)
        tags.add_tags_to_active_note(driver, data)
        tags.create_tag_via_dedicated_page(driver, data)
        tags.rename_tag(driver, data)
        dashboard.verify_dashboard(driver)
        tags.delete_tag(driver, data)
        dashboard.verify_dashboard(driver)
        search.perform_global_search(driver, data)
        dashboard.go_to_dashboard(driver)
        profile.update_name(driver, data)
        profile.change_password(driver, data)
        users.logout(driver)
        users.login_new_password(driver, data)
        profile.delete_account(driver)
        time.sleep(3)

    except Exception as e:
        print(f"Erro Crítico na execução: {e}")
    finally:
        driver.quit()
