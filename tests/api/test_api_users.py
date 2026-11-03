import pytest
from utils.api_client import ApiClient
from utils.logger import get_logger

logger = get_logger(__name__)

# URL base para ReqRes API
BASE_URL = "https://reqres.in/api"

@pytest.fixture
def api_client():
    """Fixture que retorna una instancia de ApiClient configurada con la URL base."""
    return ApiClient(BASE_URL)

@pytest.mark.api
def test_get_users(api_client):
    """
    Valida que el endpoint GET /users retorne un status code 200,
    contenga la clave 'data' y que 'data' sea una lista.
    """
    logger.info("Ejecutando test_get_users.")
    response = api_client.get("users", params={"page": 1})
    
    assert response.status_code == 200, f"Se esperaba status code 200, se obtuvo {response.status_code}"
    
    json_data = response.json()
    assert "data" in json_data, "La respuesta de la API no contiene la clave 'data'."
    assert isinstance(json_data["data"], list), "El campo 'data' no es una lista."
    assert len(json_data["data"]) > 0, "La lista de usuarios está vacía."
    
    logger.info("test_get_users completado exitosamente.")

@pytest.mark.api
def test_create_user(api_client):
    """
    Valida que el endpoint POST /users cree un usuario con éxito (status 201)
    y retorne un ID generado junto con los datos enviados.
    """
    logger.info("Ejecutando test_create_user.")
    payload = {
        "name": "Cristian Purpura",
        "job": "QA Automation / Logistics"
    }
    
    response = api_client.post("users", json=payload)
    
    assert response.status_code == 201, f"Se esperaba status code 201, se obtuvo {response.status_code}"
    
    json_data = response.json()
    assert "id" in json_data, "La respuesta no contiene el campo 'id' generado."
    assert json_data["name"] == payload["name"], "El nombre devuelto no coincide con el enviado."
    assert json_data["job"] == payload["job"], "El trabajo devuelto no coincide con el enviado."
    
    # Guardar ID para posible uso o referencia
    user_id = json_data["id"]
    logger.info(f"Usuario creado exitosamente con ID: {user_id}")
    
    # Almacenarlo en el objeto request/pytest o test para usarlo si se requiere
    pytest.created_user_id = user_id

@pytest.mark.api
def test_delete_user(api_client):
    """
    Valida que el endpoint DELETE /users/{id} elimine el usuario
    retornando un status code 204. Utiliza el ID creado previamente o '2' como fallback.
    """
    logger.info("Ejecutando test_delete_user.")
    
    # Obtener el ID generado en el test anterior o usar '2' como fallback
    user_id = getattr(pytest, "created_user_id", "2")
    logger.info(f"Eliminando usuario con ID: {user_id}")
    
    response = api_client.delete(f"users/{user_id}")
    
    # ReqRes API responde con 204 No Content al eliminar
    assert response.status_code == 204, f"Se esperaba status code 204, se obtuvo {response.status_code}"
    logger.info(f"Usuario con ID {user_id} eliminado exitosamente.")
