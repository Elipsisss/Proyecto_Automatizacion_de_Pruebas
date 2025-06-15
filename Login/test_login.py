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



def test_login_correcto(driver):
    print("Iniciando driver")
    driver.get("http://demoblaze.com/")

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


    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "nameofuser"))
    )

    texto = driver.find_element(By.ID, "nameofuser").text.lower()
    assert "diegodiegodiego123" in texto


def test_login_usuario_invalido(driver):
    print("Iniciando driver")
    driver.get("http://demoblaze.com/")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login2"))
    ).click()

    print("Ingresando usuario")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginusername"))
    ).send_keys("DiegoDiegoDiego123")

    print("Ingresando contraseña incorrecta")
    driver.find_element(By.ID, "loginpassword").send_keys("ContraseñaIncorrecta")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='logInModal']/div/div/div[3]/button[2]"))
    ).click()

    print("Validando mensaje de error")
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    mensaje_alerta = alert.text
    assert len(mensaje_alerta) > 0
    alert.accept()

    try:
        user_element = driver.find_element(By.ID, "nameofuser")
        assert not user_element.is_displayed()
    except NoSuchElementException:
        pass


def test_login_cerrar_sesion(driver):
    print("Iniciando driver")
    driver.get("http://demoblaze.com/")
    time.sleep(1)  

    driver.find_element(By.ID, "login2").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginusername"))
    )

    print("Ingresando usuario")
    driver.find_element(By.ID, "loginusername").send_keys("DiegoDiegoDiego123")
    print("Ingresando contraseña")
    driver.find_element(By.ID, "loginpassword").send_keys("DiegoDiegoDiego123")

    driver.find_element(By.XPATH, "//*[@id='logInModal']/div/div/div[3]/button[2]").click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "nameofuser"))
    )

    print("Cerrando sesión")
    driver.find_element(By.ID, "logout2").click()

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "login2"))
        )
    except TimeoutException:
        assert False


def test_login_contrasena_incorrecta(driver):
    print("Iniciando driver")
    driver.get("http://demoblaze.com/")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login2"))
    ).click()

    print("Ingresando usuario")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginusername"))
    ).send_keys("DiegoDiegoDiego123")

    print("Ingresando contraseña incorrecta")
    driver.find_element(By.ID, "loginpassword").send_keys("ContraseñaIncorrecta")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='logInModal']/div/div/div[3]/button[2]"))
    ).click()

    print("Validando mensaje de error")
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    mensaje_alerta = alert.text
    assert len(mensaje_alerta) > 0
    alert.accept()

    try:
        user_element = driver.find_element(By.ID, "nameofuser")
        assert not user_element.is_displayed()
    except NoSuchElementException:
        pass


def test_login_usuario_no_registrado(driver):
    print("Iniciando driver")
    driver.get("http://demoblaze.com/")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "login2"))
    ).click()

    print("Ingresando usuario")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "loginusername"))
    ).send_keys("UsuarioNoRegistrado")

    print("Ingresando contraseña incorrecta")
    driver.find_element(By.ID, "loginpassword").send_keys("ContraseñaIncorrecta")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='logInModal']/div/div/div[3]/button[2]"))
    ).click()

    print("Validando mensaje de error")
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    mensaje_alerta = alert.text
    assert len(mensaje_alerta) > 0
    alert.accept()

    try:
        user_element = driver.find_element(By.ID, "nameofuser")
        assert not user_element.is_displayed()
    except NoSuchElementException:
        pass



