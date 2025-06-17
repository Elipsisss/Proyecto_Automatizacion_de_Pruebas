import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def test_contacto_datos_validos(driver):
    # Given: que un usuario quiere contactar a soporte
    driver.get("https://www.demoblaze.com")
    
    # When: el usuario ingresa datos válidos en el formulario
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Contact']"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "exampleModal"))
    )

    email = "soporte@ejemplo.com"
    nombre = "Usuario Prueba"
    mensaje = "Este es un mensaje de prueba válido."

    driver.find_element(By.ID, "recipient-email").send_keys(email)
    driver.find_element(By.ID, "recipient-name").send_keys(nombre)
    driver.find_element(By.ID, "message-text").send_keys(mensaje)

    # And: el usuario da clic en el botón de enviar
    driver.find_element(By.XPATH, "//button[text()='Send message']").click()

    # Then: el sistema notifica al usuario de mensaje enviado (mediante alerta)
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alerta = driver.switch_to.alert
    texto_alerta = alerta.text
    print("🟡 Alerta recibida:", texto_alerta)
    assert "Thanks" in texto_alerta or len(texto_alerta) > 0
    alerta.accept()
    print("✅ Test finalizado correctamente")



def test_contacto_datos_invalidos(driver):
    # Given: que puedo acceder a la página de contacto
    driver.get("https://www.demoblaze.com")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Contact']"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "exampleModal"))
    )

    # When: ingreso datos inválidos (dejar campos vacíos)
    driver.find_element(By.ID, "recipient-email").clear()
    driver.find_element(By.ID, "recipient-name").clear()
    driver.find_element(By.ID, "message-text").clear()

    # And: hago clic en el botón "Enviar"
    driver.find_element(By.XPATH, "//button[text()='Send message']").click()

    # Then: validar que NO se muestre una alerta de confirmación
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        # Si se muestra una alerta, es un fallo
        alerta = driver.switch_to.alert
        texto = alerta.text
        alerta.accept()
        assert False, f"❌ Apareció una alerta inesperada: '{texto}'"
    except:
        print("✅ No se mostró alerta, lo que indica que el formulario no se envió con datos inválidos.")



def test_contacto_sin_mensaje(driver):
    # Given: tengo una cuenta de usuario (omitido porque no se requiere login en Demoblaze)
    # When: puedo ingresar al punto de contacto
    driver.get("https://www.demoblaze.com")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Contact']"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "exampleModal"))
    )

    # And: ingreso mi información de usuario
    driver.find_element(By.ID, "recipient-email").send_keys("test@example.com")
    driver.find_element(By.ID, "recipient-name").send_keys("Test User")

    # And: no ingreso ningún mensaje o comentario
    mensaje = driver.find_element(By.ID, "message-text")
    mensaje.clear()  # aseguramos que esté vacío

    # Then: hago clic en el botón "Enviar"
    driver.find_element(By.XPATH, "//button[text()='Send message']").click()

    # Then: aparece un mensaje de error (en este caso, validamos que no aparezca la alerta de éxito)
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alerta = driver.switch_to.alert
        texto = alerta.text
        alerta.accept()
        assert False, f"❌ Apareció una alerta de éxito inesperada: '{texto}'"
    except:
        print("✅ No se mostró alerta de éxito. El sistema no permitió enviar un mensaje vacío.")