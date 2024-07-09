from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def bnsToIpc():
    """
    Scrape data from a webpage table and save it to a CSV file.

    This function uses Selenium to scrape data from a specific webpage table and saves the extracted data to a CSV file named 'bns_to_ipc_mapping.csv'. The function first sets up the Selenium WebDriver with specific options, navigates to the target webpage, waits for the table element to be present, extracts the data from the table rows, and then writes the data to the CSV file. If any error occurs during the process, it will be printed to the console.

    Returns:
        None
    """
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    options.add_argument("start-maximized")

    with webdriver.Chrome(options=options) as driver:
        driver.get("https://cytrain.ncrb.gov.in/staticpage/web_pages/SectionTableBNS.html")

        try:
            element = WebDriverWait(driver=driver, timeout=5).until(
                EC.presence_of_element_located((By.XPATH, '//table/tbody'))
            )
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return

        rows = []

        sel = Selector(text=driver.page_source)
        for item in sel.xpath("//table/tbody/tr"):
            bns_list = item.xpath("td[1]//strong/span/text() | td[1]/p/span/text() | td[1]//strong/em/span/text()").getall()
            ipc_list = item.xpath("td[2]//strong/span/text() | td[2]/p/span/text() | td[2]//strong/em/span/text()").getall()
            
            if len(bns_list) == 0 or len(ipc_list) == 0:
                continue
        
            rows.append([bns_list[-1], ipc_list])

        csv_filename = 'bns_to_ipc_mapping.csv'

        with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["bns_list", "ipc_list"])
            writer.writerows(rows)

        print(f"Data has been written to {csv_filename}")


if __name__ == "__main__":
    bnsToIpc()