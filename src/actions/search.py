from selenium.webdriver.common.by import By

from src.utils import (
    slow_type,
    wait,
    wait_for_clickable,
    wait_for_element,
    wait_for_overlay_gone,
)


def perform_global_search(driver, data):
    wait_for_overlay_gone(driver)

    search_term = data["search"]["term"]
    expected_title_note = data["notes"]["edit_note"]["new_title"]

    try:
        search_input = wait_for_element(
            driver, (By.CSS_SELECTOR, "input[type='search']")
        )
        search_input.clear()
        slow_type(search_input, search_term)
        wait(2)

        result_xpath = f"//span[contains(text(), '{expected_title_note}')]"

        result_element = wait_for_clickable(driver, (By.XPATH, result_xpath))
        result_element.click()

        wait_for_element(
            driver, (By.XPATH, f"//h3[contains(text(), '{expected_title_note}')]")
        )
        wait(2)

    except Exception as e:
        print(f"[Search] Erro durante a busca: {e}")
