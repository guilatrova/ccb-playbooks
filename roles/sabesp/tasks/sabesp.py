import sys
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.getLogger().setLevel(logging.INFO)

BASE_URL = "https://www9.sabesp.com.br/agenciavirtual/"
SILENT = True


def log(message):
    if not SILENT:
        logging.info(message)


def create_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    return driver


def get_bills(rgi, owner):
    driver = create_driver()
    wait = WebDriverWait(driver, 15)

    def click_prosseguir():
        driver.find_element_by_xpath("//*[contains(text(), 'PROSSEGUIR')]").click()

    # Access Page
    driver.get(BASE_URL)
    log(f"Accessed {BASE_URL}")
    log(f"Page title {driver.title}")
    assert "Sabesp" in driver.title

    # Type RGI
    driver.find_element_by_css_selector("[title='Consulte seus débitos']").click()
    driver.find_element_by_id("frmhome:rgi1").send_keys(rgi)
    click_prosseguir()

    log("Submitted RGI")

    # Confirm
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "form"), owner))
    click_prosseguir()

    log("Confirmed RGI")

    # Get bills
    bills = []
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".iceDatTbl")))
    table = driver.find_element_by_css_selector(".iceDatTbl")

    rows = table.find_elements_by_tag_name("tr")
    for row in rows:
        columns = row.find_elements_by_tag_name("td")
        if columns:
            # column 0 = empty with checkbox
            bills.append({"month": columns[1].text, "due_date": columns[2].text, "value": columns[3].text})

    driver.quit()
    return bills


if __name__ == "__main__":
    rgi = sys.argv[1]
    owner = sys.argv[2]
    bills = get_bills(rgi, owner)
    for bill in bills:
        print(f"{bill['month']};{bill['due_date']};{bill['value']}")
