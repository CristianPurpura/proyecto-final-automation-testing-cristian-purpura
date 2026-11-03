from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple, Optional
import time
from utils.logger import get_logger

logger = get_logger(__name__)

class BasePage:
    """
    Clase base para el patrón Page Object Model (POM).
    Proporciona métodos genéricos (wrappers) con esperas explícitas y manejo de errores.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        """
        Inicializa la instancia de BasePage.

        Args:
            driver (WebDriver): Instancia del navegador de Selenium.
            timeout (int): Tiempo máximo de espera explícita en segundos (por defecto 10).
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(self.driver, self.timeout)

    def _find_element(self, by: str, locator: str) -> Optional[WebElement]:
        """
        Método interno para encontrar un elemento utilizando espera explícita.

        Args:
            by (str): Estrategia de localización (ej. By.ID, By.XPATH).
            locator (str): Valor del localizador.

        Returns:
            WebElement o None si no se encuentra.
        """
        try:
            return self.wait.until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            logger.error(f"Timeout al buscar el elemento con localizador ({by}, {locator}) tras {self.timeout} segundos.")
            return None

    def click_element(self, by: str, locator: str) -> None:
        """
        Hace clic en un elemento web después de asegurar que sea clickeable y centrarlo en pantalla.

        Args:
            by (str): Estrategia de localización.
            locator (str): Valor del localizador.
        """
        try:
            element = self.wait.until(EC.presence_of_element_located((by, locator)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.2)
            element = self.wait.until(EC.element_to_be_clickable((by, locator)))
            element.click()
            logger.info(f"Clic realizado en el elemento ({by}, {locator}).")
        except TimeoutException:
            logger.error(f"El elemento ({by}, {locator}) no estuvo disponible para clic tras {self.timeout} segundos.")
            raise

    def input_text(self, by: str, locator: str, text: str) -> None:
        """
        Limpia e introduce texto en un campo de entrada (input/textarea) evitando condiciones de carrera.

        Args:
            by (str): Estrategia de localización.
            locator (str): Valor del localizador.
            text (str): Texto a introducir.
        """
        try:
            element = self.wait.until(EC.presence_of_element_located((by, locator)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element = self.wait.until(EC.element_to_be_clickable((by, locator)))
            element.click()
            element.clear()
            element.send_keys(text)
            logger.info(f"Texto introducido en el elemento ({by}, {locator}): '{text}'.")
        except TimeoutException:
            logger.error(f"El campo de texto ({by}, {locator}) no estuvo disponible para interactuar tras {self.timeout} segundos.")
            raise

    def get_text(self, by: str, locator: str) -> str:
        """
        Obtiene el texto visible de un elemento web.

        Args:
            by (str): Estrategia de localización.
            locator (str): Valor del localizador.

        Returns:
            str: Texto contenido en el elemento.
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located((by, locator)))
            text = element.text
            logger.info(f"Texto obtenido del elemento ({by}, {locator}): '{text}'.")
            return text
        except TimeoutException:
            logger.error(f"No se pudo obtener el texto del elemento ({by}, {locator}) por timeout de {self.timeout} segundos.")
            raise

    def is_element_visible(self, by: str, locator: str) -> bool:
        """
        Verifica si un elemento es visible en la página.

        Args:
            by (str): Estrategia de localización.
            locator (str): Valor del localizador.

        Returns:
            bool: True si el elemento es visible, False en caso contrario.
        """
        try:
            self.wait.until(EC.visibility_of_element_located((by, locator)))
            logger.info(f"El elemento ({by}, {locator}) es visible.")
            return True
        except TimeoutException:
            logger.warning(f"El elemento ({by}, {locator}) no es visible tras {self.timeout} segundos.")
            return False