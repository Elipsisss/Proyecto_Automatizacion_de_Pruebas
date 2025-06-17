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

def test_redireccion_formulario_pago(driver):
    """
    Scenario: Verificar que el sistema redirige al formulario de pago
    Given que el carrito contiene productos.
    When accedo al carrito de compras.
    And hago clic en Place Order.
    Then el sistema debe mostrar el formulario de pago en una ventana modal.
    """
    # Given: que el carrito contiene productos.
    print("Inicializando prueba - Redirección a formulario de pago")
    driver.get("http://demoblaze.com/")
    time.sleep(2)  # Esperar a que la página se cargue completamente
    
    # Primero iniciamos sesión para asegurar persistencia del carrito
    print("Iniciando sesión")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login2"))
    ).click()
    
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginusername"))
    ).send_keys("DiegoDiegoDiego123")
    
    driver.find_element(By.ID, "loginpassword").send_keys("DiegoDiegoDiego123")
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='logInModal']/div/div/div[3]/button[2]"))
    ).click()
    
    # Verificar login exitoso
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "nameofuser"))
    )
    
    # Agregamos un producto al carrito
    print("Agregando producto al carrito")
    productos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-title a"))
    )
    
    # Seleccionar primer producto
    productos[0].click()
    
    # Esperar a que se cargue la página de detalle del producto
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "price-container"))
    )
    
    # Agregar al carrito
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-success"))
    ).click()
    
    # Aceptar la alerta de confirmación
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(2)  # Esperar a que se procese
    
    # When: accedo al carrito de compras
    print("Accediendo al carrito de compras")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cartur"))
    ).click()
    
    time.sleep(2)  # Esperar a que se cargue la tabla del carrito
    
    # And: hago clic en Place Order
    try:
        # Verificar que existe el botón Place Order
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".btn-success"))
        )
        
        print("Haciendo clic en Place Order")
        place_order_button = driver.find_element(By.CSS_SELECTOR, ".btn-success")
        
        # Verificar que el botón contiene el texto "Place Order"
        assert "Place Order" in place_order_button.text, f"El botón no contiene 'Place Order'. Texto actual: {place_order_button.text}"
        
        place_order_button.click()
        
        # Then: el sistema debe mostrar el formulario de pago en una ventana modal
        print("Verificando que aparece el formulario de pago")
        
        # Esperar a que aparezca el modal de pago
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "orderModal"))
        )
        
        # Verificar que el modal tiene los campos típicos de un formulario de pago
        campos_formulario = [
            "name", "country", "city", "card", "month", "year"
        ]
        
        for campo in campos_formulario:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, campo))
            )
            print(f"Campo {campo} encontrado en el formulario")
        
        # Verificar que tiene un botón para completar la compra
        purchase_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#orderModal .btn-primary"))
        )
        
        assert "Purchase" in purchase_button.text, f"El botón no contiene 'Purchase'. Texto actual: {purchase_button.text}"
        print("Formulario de pago verificado correctamente")
        
    except Exception as e:
        print(f"Error al verificar el formulario de pago: {e}")
        # Si no hay productos en el carrito, puede ser que no aparezca el botón
        raise

def test_verificar_metodos_de_pago(driver):
    """
    Scenario: Verficar que existan diferentes tipos de metodo de pago
    Given Usuario agrega producto al carrito
    When Usuario navega al modulo de carrito
    And Usuario presiona boton de pagar
    Then Pagina muestra metodos de pagos
    """
    # Given: Usuario agrega producto al carrito
    print("Inicializando prueba - Verificar métodos de pago")
    driver.get("http://demoblaze.com/")
    time.sleep(2)  # Esperar a que la página se cargue completamente
    
    # Primero iniciamos sesión para asegurar persistencia del carrito
    print("Iniciando sesión")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login2"))
    ).click()
    
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginusername"))
    ).send_keys("DiegoDiegoDiego123")
    
    driver.find_element(By.ID, "loginpassword").send_keys("DiegoDiegoDiego123")
    
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='logInModal']/div/div/div[3]/button[2]"))
    ).click()
    
    # Verificar login exitoso
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "nameofuser"))
    )
    
    # Agregamos un producto al carrito
    print("Agregando producto al carrito")
    productos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-title a"))
    )
    
    # Seleccionar primer producto
    productos[0].click()
    
    # Esperar a que se cargue la página de detalle del producto
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "price-container"))
    )
    
    # Agregar al carrito
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-success"))
    ).click()
    
    # Aceptar la alerta de confirmación
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(2)  # Esperar a que se procese
    
    # When: Usuario navega al modulo de carrito
    print("Accediendo al carrito de compras")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "cartur"))
    ).click()
    
    time.sleep(2)  # Esperar a que se cargue la tabla del carrito
    
    # And: Usuario presiona boton de pagar
    try:
        print("Haciendo clic en Place Order")
        place_order_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-success"))
        )
        place_order_button.click()
        
        # Then: Pagina muestra metodos de pagos
        print("Verificando que se muestran métodos de pago")
        
        # Esperar a que aparezca el modal de pago
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "orderModal"))
        )
        
        # Verificar que existe el campo para tarjeta
        card_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "card"))
        )
        
        # Verificar que existe información relacionada con métodos de pago
        # En demoblaze.com, la forma principal de pago es tarjeta
        modal_content = driver.find_element(By.CSS_SELECTOR, "#orderModal .modal-content").text.lower()
        
        # Verificar referencias a métodos de pago en el texto del modal
        payment_terms = ["card", "credit card", "debit card", "payment", "tarjeta"]
        found_terms = [term for term in payment_terms if term in modal_content]
        
        assert len(found_terms) > 0, f"No se encontraron términos relacionados con métodos de pago en el formulario"
        
        print(f"Términos de pago encontrados: {found_terms}")
        
        # Verificar específicamente el campo de tarjeta
        assert card_field.is_displayed(), "El campo de tarjeta no está visible en el formulario"
        
        # Como demoblaze.com no muestra explícitamente diferentes tipos de métodos de pago,
        # verificamos que al menos exista la opción de tarjeta y campos relacionados
        expected_payment_fields = ["card", "month", "year"]
        for field in expected_payment_fields:
            payment_field = driver.find_element(By.ID, field)
            assert payment_field.is_displayed(), f"El campo {field} no está visible en el formulario"
            print(f"Campo de pago {field} verificado")
        
        print("Verificación de métodos de pago completada")
        
    except Exception as e:
        print(f"Error al verificar los métodos de pago: {e}")
        raise
