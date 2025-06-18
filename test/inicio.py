from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Corregir la ruta del chromedriver
service = Service(r'C:\Program Files\chromedriver-win64\chromedriver.exe')

# Configura el navegador
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

# Inicia el navegador
driver = webdriver.Chrome(service=service, options=options)

try:
    # 1. Abre la página principal
    driver.get("http://127.0.0.1:8000/inicio")
    
    # Esperar a que la página cargue completamente
    time.sleep(2)

    # 2. Verifica que el título BIENVENIDO esté presente (texto corregido)
    titulo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'BIENVENIDO')]"))
    )
    print("✅ Título encontrado:", titulo.text)

    # 3. Verifica el botón principal "Tomar Pedido" (selector mejorado)
    boton_pedido = driver.find_element(By.CSS_SELECTOR, "a.botonPedido")
    print("✅ Botón 'Tomar Pedido' detectado")

    # Resto del código permanece igual...
    # 4. Clic en "Tomar Pedido" (redirige a otra vista)
    boton_pedido.click()
    time.sleep(2)
    print("✅ Redirección a 'Tomar Pedido' ejecutada")

    # 5. Volver al inicio
    driver.back()
    time.sleep(2)

    # 6. Probar enlaces del navbar
    enlaces = {
        "Inicio": "inicio",
        "Productos": "adminProductos",
        "Topics": "adminTopics",
        "Pedidos": "showOrdersTaken",
        "Ventas del día": "AllOrders"
    }

    for nombre, url_tag in enlaces.items():
        try:
            link = driver.find_element(By.XPATH, f"//a[contains(@href, '{url_tag}')]")
            print(f"✅ Enlace '{nombre}' encontrado")
            link.click()
            time.sleep(1)
            driver.back()
            time.sleep(1)
        except NoSuchElementException:
            print(f"❌ Enlace '{nombre}' no encontrado")

    # 7. Validar existencia de íconos animados (ej. 🐟, 🦐, 🐙)
    # Nota: No veo estos emojis en tu HTML, ¿están en otro lugar?
    for emoji in ['🐟', '🦐', '🐙']:
        try:
            driver.find_element(By.XPATH, f"//*[contains(text(), '{emoji}')]")
            print(f"✅ Ícono {emoji} detectado")
        except NoSuchElementException:
            print(f"❌ Ícono {emoji} no detectado")

    # 8. Validar acceso a las tarjetas rápidas
    # Nota: No veo estas tarjetas en tu HTML, ¿están en otro lugar?
    tarjetas = ["Menú del Mar", "Frutas Frescas", "Estadísticas"]
    for texto in tarjetas:
        try:
            driver.find_element(By.XPATH, f"//*[contains(text(), '{texto}')]")
            print(f"✅ Tarjeta '{texto}' detectada")
        except NoSuchElementException:
            print(f"❌ Tarjeta '{texto}' no detectada")

finally:
    print("\n🚀 Pruebas completadas.")
    time.sleep(3)
    driver.quit()