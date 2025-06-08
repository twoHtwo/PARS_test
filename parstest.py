from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import sleep

# Настройки драйвера
UA = UserAgent()
options = webdriver.FirefoxOptions()
# options.add_argument('--headless')  # если нужно без графического интерфейса
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", "/tmp")
options.set_preference("browser.helperApps.alwaysAsk.force", False)
options.set_preference("security.insecure_field_warning.contextual.enabled", False)
options.set_preference("dom.webnotifications.enabled", False)
options.set_preference("general.useragent.override", f"{UA.random}")

driver = webdriver.Firefox(options=options)

def take_ID():
    cor = []
    QU = input("ЗАПРОС: ")
    CO = int(input("КОЛЛ СТРАНИЦ: "))
    try:
        for i in range(1, CO + 1):
            driver.get(f"https://megamarket.ru/catalog/page-{i}/?q={QU}")
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'catalog-item-regular-desktop')))
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            cards = soup.find_all('div', class_='catalog-item-regular-desktop ddl_product catalog-item-desktop')
            for card in cards:
                product_id = card.get('data-product-id')
                if product_id:
                    cor.append(product_id)
        print(f"Найденные ID: {cor}")
        return cor
    except Exception as e:
        print(f"Ошибка в take_ID: {e}")
        return []
        
def fetch_product_details(product_ids):
    for pid in product_ids:
        try:
            driver.get(f"https://megamarket.ru/catalog/?q={pid}")
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pdp-header__title')))
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            
            name_tag = soup.find('h1', class_='pdp-header__title pdp-header__title_only-title')
            price_tag = soup.find('span', class_='sales-block-offer-price__price-final')
            
            name = name_tag.text.strip() if name_tag else 'Нет названия'
            price = price_tag.text.strip() if price_tag else 'Нет цены'
            
            print(f"ID: {pid} | Название: {name} | Цена: {price}")
        except Exception as e:
            print(f"Ошибка при обработке товара ID {pid}: {e}")

if __name__ == "__main__":
    product_ids = take_ID()
    if product_ids:
        fetch_product_details(product_ids)
    driver.quit()