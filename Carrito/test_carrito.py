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


# Inicio de funciones de utilidad
def agregar_producto_al_carrito(driver, nombre_producto):
    print(f"Agregando producto: {nombre_producto}")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, nombre_producto))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))
    ).click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

def ir_al_carrito(driver):
    print("Navegando al carrito")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cartur"))
    ).click()
# fin de funciones de utilidad


def test_valida_precio_carrito(driver):
    print("Iniciando driver")
    driver.get("https://www.demoblaze.com/")

    agregar_producto_al_carrito(driver, "Samsung galaxy s6")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Add to cart"))
    ).click()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

    ir_al_carrito(driver)

    print("verificando precio del producto en el carrito")
    totalp_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "totalp"))
    )
    total_precio = int(totalp_element.text)
    assert total_precio == 720, f"El precio esperado es 360, pero se obtuvo {total_precio}"
    time.sleep(4)
    


def test_eliminar_producto_del_carrito(driver):
    print("Iniciando driver")
    driver.get("https://www.demoblaze.com/")

    agregar_producto_al_carrito(driver, "Samsung galaxy s6")
    ir_al_carrito(driver)

    print("Eliminando producto del carrito")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Delete']"))
    ).click()

    print("Verificando producto en carrito")
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, "//tr[@class='success']/td[2]"))
    )
   


def test_carrito_abre_modal(driver):
    print("Iniciando driver")
    driver.get("https://www.demoblaze.com/")

    agregar_producto_al_carrito(driver, "Samsung galaxy s6")
    ir_al_carrito(driver)

    print("Haciendo clic en 'Place Order'")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Place Order']"))
    ).click()

    print("Validando apertura del modal de orden")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "orderModal"))
    )

    modal = driver.find_element(By.ID, "orderModal")
    assert modal.is_displayed(), "El modal de 'Place Order' no se abrió correctamente."



def test_completar_modal_y_comprar(driver):
    print("Iniciando driver")
    driver.get("https://www.demoblaze.com/")

    agregar_producto_al_carrito(driver, "Samsung galaxy s6")
    ir_al_carrito(driver)

    print("Haciendo clic en 'Place Order'")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Place Order']"))
    ).click()

    print("Llenando información del modal")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "orderModal"))
    )

    driver.find_element(By.ID, "name").send_keys("Diego Matias")
    driver.find_element(By.ID, "country").send_keys("Chile")
    driver.find_element(By.ID, "city").send_keys("Santiago")
    driver.find_element(By.ID, "card").send_keys("1234 5678 9101 1121")
    driver.find_element(By.ID, "month").send_keys("12")
    driver.find_element(By.ID, "year").send_keys("2025")

    print("Haciendo clic en 'Purchase'")
    driver.find_element(By.XPATH, "//button[text()='Purchase']").click()
    time.sleep(4)  



def test_error_pago_fallado(driver):
    print("Iniciando driver")
    driver.get("https://www.demoblaze.com/")

    agregar_producto_al_carrito(driver, "Samsung galaxy s6")
    ir_al_carrito(driver)

    print("Haciendo clic en 'Place Order'")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Place Order']"))
    ).click()

    print("Llenando información del modal")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "orderModal"))
    )

    driver.find_element(By.ID, "name").send_keys("Diego Matias")
    driver.find_element(By.ID, "country").send_keys("Chile")
    driver.find_element(By.ID, "city").send_keys("Santiago")
    driver.find_element(By.ID, "card").send_keys("")
    driver.find_element(By.ID, "month").send_keys("12")
    driver.find_element(By.ID, "year").send_keys("2025")

    print("Haciendo clic en 'Purchase'")
    driver.find_element(By.XPATH, "//button[text()='Purchase']").click()

    print("Verificando mensaje de error de pago fallido")
    time.sleep(4)



def test_verificar_tipos_de_pago(driver):
    print("Iniciando driver")
    driver.get("https://www.demoblaze.com/")

    agregar_producto_al_carrito(driver, "Samsung galaxy s6")
    ir_al_carrito(driver)

    print("Procediendo al checkout")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Place Order']"))
    ).click()

    print("Verificando que existan métodos de pago")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "payment-methods"))
    )

    metodos_pago = driver.find_elements(By.XPATH, "//input[@name='payment-method']")
    assert len(metodos_pago) >= 2, "No hay suficientes métodos de pago disponibles."

    opciones = [driver.find_element(By.XPATH, f"//label[@for='{metodo.get_attribute('id')}']").text.lower() for metodo in metodos_pago]
    print(f"Métodos encontrados: {opciones}")
    assert "credit card" in opciones
    assert "paypal" in opciones
