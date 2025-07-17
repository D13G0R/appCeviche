from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import os
from datetime import datetime

# Configuración del driver
service = Service(r'C:\Program Files\chromedriver-win64\chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(service=service, options=options)

# Configuración de capturas de pantalla
SCREENSHOTS_DIR = "test_screenshots"
if not os.path.exists(SCREENSHOTS_DIR):
    os.makedirs(SCREENSHOTS_DIR)

def take_screenshot(name):
    """Toma captura de pantalla y la guarda con nombre descriptivo"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{SCREENSHOTS_DIR}/{name}_{timestamp}.png"
        driver.save_screenshot(filename)
        print(f"📸 Captura guardada: {filename}")
        return filename
    except Exception as e:
        print(f"⚠️ Error al tomar captura: {str(e)}")
        return None

def wait_and_see(seconds=3, message=""):
    """Espera visualmente con mensaje descriptivo"""
    try:
        if message:
            print(f"⏳ {message} (esperando {seconds} segundos...)")
        time.sleep(seconds)
    except Exception as e:
        print(f"⚠️ Error en wait_and_see: {str(e)}")

def verificar_pagina_cargada(timeout=10):
    """Verifica que la página haya cargado completamente"""
    print("🔍 Verificando carga completa de la página...")
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        return True
    except TimeoutException:
        print("⚠️ La página tardó demasiado en cargar")
        return False
    except Exception as e:
        print(f"⚠️ Error al verificar carga de página: {str(e)}")
        return False

def probar_boton_tomar_pedido():
    """Función para probar el botón Tomar Pedido"""
    try:
        print("\n" + "="*50)
        print("🔘 PROBANDO BOTÓN 'TOMAR PEDIDO'")
        print("="*50)
        
        boton_pedido = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//div[contains(text(), '🍽️')]]"))
        )
        print("✅ Botón 'Tomar Pedido' detectado")
        
        current_url = driver.current_url
        take_screenshot("02_antes_de_clic_tomar_pedido")

        print("🖱️ Haciendo clic en 'Tomar Pedido'...")
        boton_pedido.click()
        wait_and_see(2, "Cargando página de pedidos")

        WebDriverWait(driver, 5).until(EC.url_changes(current_url))
        take_screenshot("03_pagina_tomar_pedido")
        
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "body")))
            print("✅ Página de 'Tomar Pedido' cargada correctamente")
            print(f"📌 URL actual: {driver.current_url}")
            
            wait_and_see(5, "Observando página de pedidos")
            
        except Exception as e:
            print(f"⚠️ No se pudo verificar contenido de la página: {str(e)}")

        print("↩️ Regresando a página principal...")
        driver.back()
        WebDriverWait(driver, 5).until(EC.url_to_be(current_url))
        take_screenshot("04_regreso_a_principal")
        wait_and_see(3, "Página principal recargada")
        print("✅ Regreso a página principal exitoso")
        
    except Exception as e:
        print(f"❌ Error con botón 'Tomar Pedido': {str(e)}")
        take_screenshot("error_boton_tomar_pedido")

def probar_enlace(nombre, texto, url_esperada):
    """Función para probar un enlace específico"""
    try:
        print("\n" + "="*50)
        print(f"🔗 PROBANDO ENLACE: {nombre}")
        print("="*50)
        
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{texto}')]"))
        )
        print(f"✅ Enlace '{nombre}' encontrado")
        take_screenshot(f"05_antes_de_{nombre.lower().replace(' ', '_')}")
        
        main_url = driver.current_url
        
        print(f"🖱️ Haciendo clic en '{nombre}'...")
        link.click()
        wait_and_see(2, f"Cargando página de {nombre}")
        
        WebDriverWait(driver, 10).until(EC.url_changes(main_url))
        take_screenshot(f"06_pagina_{nombre.lower().replace(' ', '_')}")
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body")))
            print(f"✅ Página de '{nombre}' cargada correctamente")
            print(f"📌 URL actual: {driver.current_url}")
            
            wait_and_see(2, f"Observando página de {nombre}")
            
            if url_esperada in driver.current_url:
                print(f"✅ URL correcta para '{nombre}'")
            else:
                print(f"⚠️ URL inesperada. Esperaba '{url_esperada}', obtuve '{driver.current_url}'")
            
        except Exception as e:
            print(f"⚠️ No se pudo verificar contenido de la página: {str(e)}")

        print(f"↩️ Regresando a página principal desde {nombre}...")
        driver.back()
        WebDriverWait(driver, 5).until(EC.url_to_be(main_url))
        take_screenshot(f"07_regreso_desde_{nombre.lower().replace(' ', '_')}")
        wait_and_see(3, "Página principal recargada")
        print("✅ Regreso a página principal exitoso")
        
    except Exception as e:
        print(f"❌ Error con enlace '{nombre}': {str(e)}")
        take_screenshot(f"error_enlace_{nombre.lower().replace(' ', '_')}")
        driver.get("http://127.0.0.1:8000/inicio")
        wait_and_see(2, "Recargando página principal")

try:
    # 1. Abrir la página principal
    print("\n" + "="*50)
    print("🚀 INICIANDO PRUEBAS - PÁGINA PRINCIPAL")
    print("="*50)
    
    driver.get("http://127.0.0.1:8000/inicio")
    take_screenshot("00_pagina_principal_inicio")
    wait_and_see(2, "Página principal cargando")

    if not verificar_pagina_cargada():
        print("⚠️ Advertencia: La página podría no haber cargado completamente")

    # 2. Verificar el título principal
    try:
        titulo = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), '¡BIENVENIDO!')]"))
        )
        print(f"✅ Título encontrado: {titulo.text}")
        take_screenshot("01_titulo_principal")
    except Exception as e:
        print(f"❌ Error al verificar título principal: {str(e)}")

    # 3. Probar botón "Tomar Pedido"
    probar_boton_tomar_pedido()

    # 4. Probar enlaces del navbar
    enlaces_nav = {
        "Productos": ("🍤 Productos", "/showProductos/"),
        "Topics": ("📋 Topics", "/showTopics/"),
        "Pedidos": ("🛒 Pedidos", "/showOrdersTaken/"),
        "Ventas del día": ("💰 Ventas del día", "/showAllOrders/")
    }

    for nombre, (texto, url_esperada) in enlaces_nav.items():
        probar_enlace(nombre, texto, url_esperada)

    # 5. Verificación final de elementos visuales
    print("\n" + "="*50)
    print("👀 VERIFICACIÓN FINAL DE ELEMENTOS VISUALES")
    print("="*50)
    
    wait_and_see(2, "Finalizando pruebas")
    take_screenshot("08_finalizacion_pruebas")

except Exception as e:
    print(f"\n❌❌❌ ERROR GRAVE: {str(e)}")
    take_screenshot("error_fatal")
finally:
    print("\n" + "="*50)
    print("🏁 PRUEBAS COMPLETADAS")
    print(f"📂 Capturas de pantalla guardadas en: {os.path.abspath(SCREENSHOTS_DIR)}")
    print("="*50)
    
    wait_and_see(2, "Cerrando navegador")
    driver.quit()