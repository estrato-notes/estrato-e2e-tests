from selenium.webdriver.common.by import By

from src.config import BASE_URL
from src.utils import wait


def create_quick_note(driver, data):
    note_data = data["notes"]["quick_capture"]
    content = note_data["content"]

    if "/dashboard" not in driver.current_url:
        driver.get(f"{BASE_URL}/dashboard")
        wait()

    textarea = driver.find_element(
        By.XPATH, "//textarea[@placeholder='Digite sua nota rápida aqui...']"
    )
    textarea.send_keys(content)
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
