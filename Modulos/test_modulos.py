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


def test_navegacion_entre_modulos(driver):
    # Given: que puedo acceder a la aplicación
    driver.get("https://www.demoblaze.com")

    # Lista de módulos a recorrer
    modulos = ["Phones", "Laptops", "Monitors"]

    for modulo in modulos:
        # When: navego al módulo
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, modulo))
        ).click()

        # Then: el módulo debe cargar correctamente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "card"))
        )
        productos = driver.find_elements(By.CLASS_NAME, "card-title")
        assert len(productos) > 0, f"No se cargaron productos en el módulo {modulo}"
        print(f"✅ Módulo '{modulo}' cargó correctamente con {len(productos)} productos.")


def test_boton_next_en_categoria(driver):
    # Given: que el usuario está en una categoría de producto
    driver.get("https://www.demoblaze.com")
    categoria = "Phones"

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, categoria))
    ).click()

    # Esperar productos de la primera página
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title"))
    )
    productos_pagina_1 = [
        elem.text for elem in driver.find_elements(By.CLASS_NAME, "card-title")
    ]

    # When: hace clic en "Next"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "next2"))
    ).click()

    # Esperar que cambien los productos
    WebDriverWait(driver, 10).until(
        lambda d: any(
            elem.text not in productos_pagina_1
            for elem in d.find_elements(By.CLASS_NAME, "card-title")
        )
    )

    productos_pagina_2 = [
        elem.text for elem in driver.find_elements(By.CLASS_NAME, "card-title")
    ]

    # Then: validar que los productos son distintos, pero sigue en la misma categoría
    assert productos_pagina_1 != productos_pagina_2, "Los productos no cambiaron tras hacer clic en 'Next'"
    assert all(productos_pagina_2), "No se cargaron productos en la segunda página"
    print(f"✅ Se cambió de página correctamente dentro de la categoría '{categoria}'.")



def test_prev_deshabilitado_en_primera_pagina(driver):
    # Given: el usuario está en una categoría de producto
    driver.get("https://www.demoblaze.com")
    categoria = "Phones"

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, categoria))
    ).click()

    # When: accede a la primera página de resultados
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title"))
    )
    productos_iniciales = [
        elem.text for elem in driver.find_elements(By.CLASS_NAME, "card-title")
    ]

    # And: el botón Prev debe estar deshabilitado visual o funcionalmente
    boton_prev = driver.find_element(By.ID, "prev2")

    # Intentamos hacer clic, pero no debería cambiar la página
    boton_prev.click()

    WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title"))
    )
    productos_post_click = [
        elem.text for elem in driver.find_elements(By.CLASS_NAME, "card-title")
    ]

    # Then: la página no debe cambiar
    assert productos_iniciales == productos_post_click, "La página cambió tras hacer clic en 'Prev' en la primera página"
    print(f"✅ El botón 'Prev' no permitió navegar desde la primera página de la categoría '{categoria}'.")
  



def test_prev_no_visible_al_ingresar(driver):
    # Given: el usuario ingresa a la página de productos
    driver.get("https://www.demoblaze.com")

    # When: el usuario busca el botón "Prev"
    try:
        boton_prev = driver.find_element(By.ID, "prev2")
        visible = boton_prev.is_displayed()
    except:
        visible = False

    # And: el botón no debe estar visible
    assert not visible, "❌ El botón 'Prev' está visible al cargar la página, pero no debería"

    # Then: si estuviera presente y se hace clic, no debe cambiar el contenido
    if visible:
        productos_pagina_1 = [
            e.text for e in driver.find_elements(By.CLASS_NAME, "card-title")
        ]
        boton_prev.click()
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card-title"))
        )
        productos_post_click = [
            e.text for e in driver.find_elements(By.CLASS_NAME, "card-title")
        ]
        assert productos_pagina_1 == productos_post_click, "❌ El botón 'Prev' cambió el contenido, pero no debería"

    print("✅ El botón 'Prev' no está visible o no hace nada al ingresar, como se esperaba.")