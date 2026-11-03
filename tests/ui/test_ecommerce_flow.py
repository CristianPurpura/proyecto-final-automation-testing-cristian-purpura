import json
import os
import time
import pytest
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage
from utils.logger import get_logger

logger = get_logger(__name__)

# Cargar datos de usuarios desde data/login_data.json
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "login_data.json")

def load_login_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.mark.ui
@pytest.mark.parametrize("user_data", load_login_data())
def test_login_parametized(driver, user_data):
    """
    Test parametrizado para validar el inicio de sesión con diferentes tipos de usuarios.
    """
    username = user_data["username"]
    password = user_data["password"]
    expected = user_data["expected_result"]

    logger.info(f"Ejecutando test_login_parametized para usuario: {username}")
    driver.get("https://www.saucedemo.com/")
    
    login_page = LoginPage(driver)
    login_page.login(username, password)

    if expected == "success":
        inventory_page = InventoryPage(driver)
        assert inventory_page.is_element_visible(*inventory_page.PAGE_TITLE), f"El usuario {username} debería haber ingresado al inventario."
        logger.info(f"Login exitoso verificado para {username}.")
    else:
        error_msg = login_page.get_error_message()
        assert expected in error_msg, f"Se esperaba el mensaje de error '{expected}', pero se obtuvo '{error_msg}'"
        logger.info(f"Mensaje de error validado correctamente para {username}: {error_msg}")

@pytest.mark.ui
def test_e2e_purchase_flow(driver):
    """
    Test End-to-End del flujo completo de compra en SauceDemo.
    """
    logger.info("Iniciando test de flujo completo E2E de compra.")
    
    # 1. Login
    driver.get("https://www.saucedemo.com/")
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")

    # 2. Agregar producto al carrito
    inventory_page = InventoryPage(driver)
    assert inventory_page.is_element_visible(*inventory_page.PAGE_TITLE), "No se pudo visualizar el inventario."
    
    product_name = "Sauce Labs Backpack"
    inventory_page.add_item_to_cart(product_name)
    inventory_page.go_to_cart()

    # Breve pausa ANTES del clic para que React active el botón del carrito
    time.sleep(1)

    # 3. Ir al Checkout y rellenar datos
    checkout_button = (By.ID, "checkout")
    inventory_page.click_element(*checkout_button)

    checkout_page = CheckoutPage(driver)
    assert checkout_page.is_checkout_form_visible(), "El formulario de checkout no cargó a tiempo."
    checkout_page.fill_shipping_info(name="Cristian", last_name="Purpura", zip_code="10001")

    # 4. Finalizar orden
    checkout_page.finish_checkout()

    # 5. Validar mensaje de éxito
    success_header_locator = (By.CLASS_NAME, "complete-header")
    success_message = checkout_page.get_text(*success_header_locator)
    
    assert "Thank you for your order!" in success_message, f"El mensaje de éxito no coincide."
    logger.info("¡Flujo E2E de compra completado y validado exitosamente!")

@pytest.mark.ui
def test_forced_failure_for_screenshot(driver):
    """
    Test diseñado deliberadamente para fallar.
    Valida la captura de pantalla automática.
    """
    logger.info("Ejecutando test_forced_failure_for_screenshot (fallo intencional).")
    driver.get("https://www.saucedemo.com/")
    
    login_page = LoginPage(driver)
    assert login_page.is_element_visible(*login_page.LOGIN_BUTTON), "El botón de login debería ser visible."
    
    logger.error("Forzando un fallo de aserción para verificar la captura de pantalla.")
    assert False, "Forzando fallo para validar la captura de pantalla en el reporte HTML."