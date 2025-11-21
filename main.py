import json
import time

from selenium import webdriver

from src.actions import dashboard, notebooks, notes, templates, users


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

        time.sleep(3)

    except Exception as e:
        print(f"Erro Crítico na execução: {e}")
    finally:
        driver.quit()
