from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class InventoryPage(BasePage):
    """
    Page Object para la página de Inventario de SauceDemo.
    """

    # Definición de selectores como tuplas (By, value)
    PAGE_TITLE = (By.CLASS_NAME, "title")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver) -> None:
        super().__init__(driver)

    def add_item_to_cart(self, item_name: str) -> None:
        """
        Añade un producto al carrito basado en su nombre visible en la interfaz.

        Args:
            item_name (str): Nombre exacto del producto (ej. 'Sauce Labs Backpack').
        """
        logger.info(f"Añadiendo al carrito el producto: {item_name}")
        # XPath robusto para encontrar el botón de añadir al carrito correspondiente al producto
        item_button_xpath = f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        self.click_element(By.XPATH, item_button_xpath)

    def go_to_cart(self) -> None:
        """
        Navega hacia la página del carrito de compras haciendo clic en el icono del carrito.
        """
        logger.info("Navegando al carrito de compras.")
        self.click_element(*self.CART_ICON)
