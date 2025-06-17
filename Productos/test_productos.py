import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
@pytest.fixture
def driver():
    options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_precio_productos_mayor_a_cero(driver):
    print("Accediendo a la web")
    driver.get("https://www.demoblaze.com")

    wait = WebDriverWait(driver, 10)

    productos = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-title a"))
    )
    
    urls_productos = [producto.get_attribute("href") for producto in productos]


    for url in urls_productos:
        print(f"Revisando producto: {url}")
        driver.get(url)

        precio_element = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "price-container"))
        )
        precio_texto = precio_element.text 
        precio_numero = float(precio_texto.split()[0].replace("$", ""))

        print(f"Precio encontrado: {precio_numero}")
        assert precio_numero > 0, f"El producto en {url} tiene precio inválido: {precio_numero}"
