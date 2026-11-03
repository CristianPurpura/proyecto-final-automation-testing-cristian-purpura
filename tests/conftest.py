import os
import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pytest_html
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.fixture
def driver():
    """Fixture global para inicializar y cerrar el WebDriver de Chrome en modo headless."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    logger.info("Inicializando Chrome WebDriver desde conftest.py.")
    driver_instance = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver_instance
    logger.info("Cerrando Chrome WebDriver desde conftest.py.")
    driver_instance.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de pytest para capturar el resultado de las pruebas.
    Si un test falla en la fase de ejecución ('call'), toma un screenshot y lo adjunta al reporte HTML.
    """
    outcome = yield
    report = outcome.get_result()

    # Verificar si el test falló durante la ejecución de la prueba
    if report.when == "call" and report.failed:
        driver_instance = item.funcargs.get("driver")
        if driver_instance:
            screenshots_dir = os.path.join(os.getcwd(), "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            safe_test_name = item.name.replace("[", "_").replace("]", "").replace("'", "")
            filename = f"{timestamp}_{safe_test_name}.png"
            filepath = os.path.join(screenshots_dir, filename)
            
            try:
                driver_instance.save_screenshot(filepath)
                logger.error(f"Test fallido: {item.name}. Screenshot guardado en: {filepath}")
                
                # Obtener la captura en formato base64 para evitar problemas de rutas absolutas / CORS en el reporte HTML
                screenshot_base64 = driver_instance.get_screenshot_as_base64()
                
                # Adjuntar screenshot en base64 al reporte HTML usando pytest_html.extras.image
                extra = getattr(report, "extras", [])
                extra.append(pytest_html.extras.image(screenshot_base64, name='Captura de Fallo'))
                report.extras = extra
            except Exception as e:
                logger.error(f"No se pudo tomar o adjuntar el screenshot para {item.name}: {e}")
