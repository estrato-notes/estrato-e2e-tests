from selenium.webdriver.common.by import By

from src.utils import slow_type, wait


def perform_global_search(driver, data):
    search_term = data["search"]["term"]
    expected_title_note = data["notes"]["edit_note"]["new_title"]

    try:
        search_input = driver.find_element(By.CSS_SELECTOR, "input[type='search']")
        search_input.clear()
        slow_type(search_input, search_term)
        wait()

        result = driver.find_elements(
            By.XPATH, f"//span[contains(text(), '{expected_title_note}')]"
        )
        result[0].click()
        wait()
    except Exception as e:
        print(f"[Search] Erro durante a busca: {e}")
