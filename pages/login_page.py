from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class LoginPage(BasePage):
    """
    Page Object para la página de Login de SauceDemo.
    """

    # Definición de selectores como tuplas (By, value)
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver) -> None:
        super().__init__(driver)

    def login(self, user: str, password: str) -> None:
        """
        Realiza el proceso de inicio de sesión ingresando usuario, contraseña y haciendo clic en login.

        Args:
            user (str): Nombre de usuario.
            password (str): Contraseña.
        """
        logger.info(f"Iniciando sesión con el usuario: {user}")
        self.input_text(*self.USERNAME_INPUT, user)
        self.input_text(*self.PASSWORD_INPUT, password)
        self.click_element(*self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """
        Obtiene el mensaje de error mostrado en la página de login.

        Returns:
            str: Texto del mensaje de error.
        """
        logger.info("Obteniendo mensaje de error de login.")
        return self.get_text(*self.ERROR_MESSAGE)
