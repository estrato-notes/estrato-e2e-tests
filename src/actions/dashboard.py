import time

from selenium.webdriver.common.by import By

from src.config import BASE_URL
from src.utils import slow_type, wait


def go_to_dashboard(driver):
    if "/dashboard" not in driver.current_url:
        driver.get(f"{BASE_URL}/dashboard")
        wait()
        time.sleep(3)


def create_quick_note(driver, data):
    note_data = data["notes"]["quick_capture"]
    content = note_data["content"]

    go_to_dashboard(driver)

    textarea = driver.find_element(
        By.XPATH, "//textarea[@placeholder='Digite sua nota rápida aqui...']"
    )
    slow_type(textarea, content)
    wait()
    wait()

    save_btn = driver.find_element(By.XPATH, "//button[contains(., 'Salvar')]")
    save_btn.click()
    wait()

    expected_start = note_data.get("expected_title_start", content[:10])
    recent_notes = driver.find_elements(
        By.XPATH, "//div[h3[contains(., '" + expected_start + "')]]"
    )

    if len(recent_notes) > 0:
        print("[Dashboard] Sucesso: Nota rápida encontrada na lista recente.")
    else:
        print("[Dashboard] Erro: Nota rápida não apareceu na lista.")


def verify_dashboard(driver):
    go_to_dashboard(driver)
    wait()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    wait()
