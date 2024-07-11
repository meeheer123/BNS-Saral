from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def bnssToCrpc():
    """
    Scrape data from a webpage table and save it to a CSV file.

    This function uses Selenium to scrape data from a specific webpage table and saves the extracted data to a CSV file named 'bnss_to_crpc_mapping.csv'. The function first sets up the Selenium WebDriver with specific options, navigates to the target webpage, waits for the table element to be present, extracts the data from the table rows, and then writes the data to the CSV file. If any error occurs during the process, it will be printed to the console.

    Returns:
        None
    """
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    options.add_argument("start-maximized")

    with webdriver.Chrome(options=options) as driver:
        driver.get("https://www.taxmann.com/post/blog/tabular-comparison-sections-of-code-of-criminal-clauses-vs-provisions-of-bharatiya-nagarik-suraksha-sanhita/")

        try:
            element = WebDriverWait(driver=driver, timeout=5).until(
                EC.presence_of_element_located((By.XPATH, '//table/tbody'))
            )
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return

        rows = []

        sel = Selector(text=driver.page_source)
        for item in sel.xpath("//table/tbody/tr")[1:]:
            section_crpc = item.xpath("td[1]//text()").get()
            heading_crpc = item.xpath("td[2]//text()").get()
            clause_bnss = item.xpath("td[3]//text()").get()
            heading_bnss = item.xpath("td[4]//text()").get()
            rows.append([section_crpc, heading_crpc, clause_bnss, heading_bnss])

        csv_filename = 'bnss_to_crpc_mapping.csv'

        with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)

        print(f"Data has been written to {csv_filename}")


if __name__ == "__main__":
    bnssToCrpc()
    