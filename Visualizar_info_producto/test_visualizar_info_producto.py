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


def test_visualizar_informacion_producto(driver):
    """
    Scenario: Verificar que la información del producto se muestra correctamente
    Given que puedo acceder a la web
    When ingreso a la página de un producto
    And verifico que el nombre, descripción, precio e imagen están visibles
    Then la información del producto debe mostrarse correctamente
    """
    # Given: que puedo acceder a la web
    print("Accediendo a la web de demoblaze")
    driver.get("http://demoblaze.com/")
    time.sleep(2)  # Esperar a que la página se cargue completamente
    
    # When: ingreso a la página de un producto
    print("Seleccionando un producto para verificar su información")
    productos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".card-title a"))
    )
    
    # Guardar el nombre del producto en la página principal para verificación posterior
    nombre_producto_lista = productos[0].text
    print(f"Producto seleccionado desde lista: {nombre_producto_lista}")
    
    # Hacer clic en el primer producto
    productos[0].click()
    
    # And: verifico que el nombre, descripción, precio e imagen están visibles
    print("Verificando elementos de información del producto")
    
    # 1. Verificar que el nombre del producto está visible
    nombre_producto = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".name"))
    )
    
    # 2. Verificar que la descripción está visible
    descripcion_producto = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#more-information p"))
    )
    
    # 3. Verificar que el precio está visible
    precio_producto = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".price-container"))
    )
      # 4. Verificar que la imagen está visible - corregimos el selector para la imagen
    try:
        # Intentamos con el selector más específico primero
        imagen_producto = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".active .item img"))
        )
    except TimeoutException:
        # Si falla, intentamos con un selector más general
        print("Intentando con selector alternativo para la imagen")
        imagen_producto = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#imgp img"))
        )
    
    # Then: la información del producto debe mostrarse correctamente
    # Verificar que el nombre del producto coincide con el que vimos en la lista
    assert nombre_producto.text.strip() == nombre_producto_lista.strip(), f"El nombre del producto no coincide: {nombre_producto.text} vs {nombre_producto_lista}"
    print(f"Nombre del producto verificado: {nombre_producto.text}")
    
    # Verificar que la descripción no está vacía
    assert len(descripcion_producto.text.strip()) > 0, "La descripción del producto está vacía"
    print(f"Descripción del producto encontrada: {descripcion_producto.text[:50]}...")
    
    # Verificar que el precio tiene formato correcto (contiene $ y un número)
    precio_texto = precio_producto.text
    assert "$" in precio_texto, f"El formato del precio es incorrecto: {precio_texto}"
    
    # Extraer el valor numérico del precio
    precio_valor = float(precio_texto.split()[0].replace("$", ""))
    assert precio_valor > 0, f"El precio debe ser mayor que cero: {precio_valor}"
    print(f"Precio verificado: {precio_texto}")
    
    # Verificar que la imagen está cargada y tiene atributos correctos
    assert imagen_producto.is_displayed(), "La imagen del producto no está visible"
    
    # Verificamos que la imagen tenga algún atributo de origen (src o data-src)
    src = imagen_producto.get_attribute("src")
    if src:
        print(f"Imagen verificada con src: {src}")
    else:
        # Intentamos con otros atributos que podrían contener la URL de la imagen
        data_src = imagen_producto.get_attribute("data-src")
        assert data_src is not None, "La imagen no tiene URL en ningún atributo"
        print(f"Imagen verificada con data-src: {data_src}")
    
    print("Todos los elementos de información del producto se muestran correctamente")


def test_disponibilidad_productos(driver):
    """
    Scenario: Verificar la disponibilidad de los productos
    Given El ususario ingresa a la pagina
    When Entra al catalogo de productos
    And Verfico la cantidad de productos en venta
    Then Deben haber a lo menos 3 tipos de productos disponibles
    """
    # Given: El usuario ingresa a la página
    print("Accediendo a la web de demoblaze")
    driver.get("http://demoblaze.com/")
    time.sleep(3)  # Aumentamos el tiempo de espera para asegurar carga completa
    
    # When: Entra al catálogo de productos (ya estamos en el catálogo por defecto)
    print("Verificando el catálogo de productos")
    
    # And: Verifico la cantidad de productos en venta
    print("Contando productos disponibles")
    
    try:
        # Esperar a que se carguen los productos
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".card"))
        )
        
        # Contar todos los productos visibles
        productos = driver.find_elements(By.CSS_SELECTOR, ".card")
        cantidad_productos = len(productos)
        
        print(f"Cantidad de productos encontrados: {cantidad_productos}")
        
        # Obtener las categorías de productos
        categorias_elementos = driver.find_elements(By.CSS_SELECTOR, ".list-group-item")
        categorias = [cat.text for cat in categorias_elementos if cat.text and cat.text.lower() != "categories"]
        
        print(f"Categorías disponibles: {categorias}")
        
        # Verificar cuántos tipos de productos hay disponibles
        # Opción 1: Por categorías visibles
        tipos_por_categorias = len(categorias)
        
        # Opción 2: Contar cuántos productos diferentes hay
        nombres_productos = set()
        for producto in productos:
            try:
                nombre = producto.find_element(By.CSS_SELECTOR, ".card-title").text
                nombres_productos.add(nombre)
            except:
                pass
        
        print(f"Productos únicos encontrados: {len(nombres_productos)}")
        print(f"Nombres de productos: {', '.join(list(nombres_productos)[:5])}...")
        
        # Then: Deben haber al menos 3 tipos de productos disponibles
        # Verificamos tanto por cantidad total como por categorías
        assert cantidad_productos >= 3, f"Hay menos de 3 productos disponibles: {cantidad_productos}"
        assert len(nombres_productos) >= 3, f"Hay menos de 3 tipos de productos diferentes: {len(nombres_productos)}"
        
        print("Verificación de disponibilidad de productos completada exitosamente")
        
    except TimeoutException:
        print("Error: Tiempo de espera agotado al buscar productos")
        assert False, "No se pudo cargar el catálogo de productos"
    except Exception as e:
        print(f"Error al verificar la disponibilidad de productos: {e}")
        assert False, f"Error en la prueba: {e}"
