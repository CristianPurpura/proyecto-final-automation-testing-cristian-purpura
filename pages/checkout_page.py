from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class CheckoutPage(BasePage):
    """
    Page Object para las páginas de Checkout de SauceDemo.
    """

    # Definición de selectores como tuplas (By, value)
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")

    def __init__(self, driver) -> None:
        super().__init__(driver)

    def is_checkout_form_visible(self) -> bool:
        """
        Verifica que el formulario de información de envío del checkout sea visible.
        """
        logger.info("Verificando que el formulario de checkout sea visible.")
        return self.is_element_visible(*self.FIRST_NAME_INPUT)

    def fill_shipping_info(self, name: str, last_name: str, zip_code: str) -> None:
        """
        Rellena la información de envío (Checkout: Your Information).
        """
        logger.info(f"Rellenando información de envío: {name} {last_name}, CP: {zip_code}")
        self.input_text(*self.FIRST_NAME_INPUT, name)
        self.input_text(*self.LAST_NAME_INPUT, last_name)
        self.input_text(*self.POSTAL_CODE_INPUT, zip_code)
        self.click_element(*self.CONTINUE_BUTTON)

    def finish_checkout(self) -> None:
        """
        Finaliza el proceso de compra haciendo clic en el botón Finish (Checkout: Overview).
        """
        logger.info("Finalizando la orden de compra.")
        self.click_element(*self.FINISH_BUTTON)