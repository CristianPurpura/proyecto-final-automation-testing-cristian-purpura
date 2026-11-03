import requests
from typing import Optional, Dict, Any
from utils.logger import get_logger

logger = get_logger(__name__)

class ApiClient:
    """
    Cliente API genérico utilizando la librería requests.
    Proporciona wrappers para peticiones HTTP (GET, POST, DELETE) con registro en logs.
    """

    def __init__(self, base_url: str) -> None:
        """
        Inicializa el ApiClient.

        Args:
            base_url (str): URL base de la API (ej. 'https://reqres.in/api').
        """
        self.base_url = base_url.rstrip("/")

    def _get_full_url(self, endpoint: str) -> str:
        """Construye la URL completa combinando base_url y endpoint."""
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        return self.base_url + endpoint

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Realiza una petición HTTP GET.

        Args:
            endpoint (str): Endpoint o ruta del recurso.
            params (dict, optional): Parámetros de consulta (Query params).
            headers (dict, optional): Cabeceras HTTP adicionales.

        Returns:
            requests.Response: Objeto de respuesta de requests.
        """
        url = self._get_full_url(endpoint)
        logger.info(f"API GET -> URL: {url} | Params: {params}")
        response = requests.get(url, params=params, headers=headers)
        logger.info(f"API RESPONSE <- Status Code: {response.status_code} | Body: {response.text[:200]}")
        return response

    def post(self, endpoint: str, data: Optional[Any] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Realiza una petición HTTP POST.

        Args:
            endpoint (str): Endpoint o ruta del recurso.
            data (any, optional): Datos de formulario.
            json (dict, optional): Payload en formato JSON.
            headers (dict, optional): Cabeceras HTTP adicionales.

        Returns:
            requests.Response: Objeto de respuesta de requests.
        """
        url = self._get_full_url(endpoint)
        logger.info(f"API POST -> URL: {url} | Payload JSON: {json} | Data: {data}")
        response = requests.post(url, data=data, json=json, headers=headers)
        logger.info(f"API RESPONSE <- Status Code: {response.status_code} | Body: {response.text[:200]}")
        return response

    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Realiza una petición HTTP DELETE.

        Args:
            endpoint (str): Endpoint o ruta del recurso.
            headers (dict, optional): Cabeceras HTTP adicionales.

        Returns:
            requests.Response: Objeto de respuesta de requests.
        """
        url = self._get_full_url(endpoint)
        logger.info(f"API DELETE -> URL: {url}")
        response = requests.delete(url, headers=headers)
        logger.info(f"API RESPONSE <- Status Code: {response.status_code}")
        return response
