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


def go_to_dashboard(driver):
    wait_for_overlay_gone(driver)
    if "/dashboard" not in driver.current_url:
        driver.get(f"{BASE_URL}/dashboard")
        wait_for_url_contains(driver, "/dashboard")
        wait()


def create_quick_note(driver, data):
    note_data = data["notes"]["quick_capture"]
    content = note_data["content"]

    go_to_dashboard(driver)

    textarea = wait_for_element(
        driver, (By.XPATH, "//textarea[@placeholder='Digite sua nota rápida aqui...']")
    )
    slow_type(textarea, content)
    wait(1)

    wait_for_clickable(driver, (By.XPATH, "//button[contains(., 'Salvar')]")).click()
    wait(2)

    expected_start = note_data.get("expected_title_start", content[:10])

    try:
        wait_for_element(
            driver, (By.XPATH, f"//div[h3[contains(., '{expected_start}')]]")
        )
        print("[Dashboard] Sucesso: Nota rápida encontrada na lista recente.")
    except Exception as e:
        print(f"[Dashboard] Erro: Nota rápida não apareceu na lista: {e}")


def verify_dashboard(driver):
    go_to_dashboard(driver)

    wait_for_element(driver, (By.XPATH, "//div[contains(@class, 'grid')]"))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    wait(2)
