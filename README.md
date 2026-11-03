# Enterprise Hybrid Test Automation Framework (UI & API)

Framework híbrido de pruebas automatizadas de nivel empresarial desarrollado en Python, diseñado para la validación de interfaces de usuario (UI) bajo el patrón **Page Object Model (POM)** y servicios Web (API REST), aplicando principios de automatización robustos, mantenibles y escalables.

---

## 🚀 Propósito del Proyecto
Este framework valida flujos críticos de negocio en plataformas de e-commerce y logística, abarcando desde la autenticación y la gestión de inventario hasta la finalización de órdenes de compra (End-to-End), complementado con pruebas de integración sobre servicios REST públicos (ReqRes API).

---

## 🛠️ Tecnologías y Librerías
- **Python 3.10+**: Lenguaje de programación principal.
- **Pytest**: Framework de ejecución y gestión de pruebas.
- **Selenium WebDriver**: Automatización de navegadores web.
- **Requests**: Cliente HTTP para automatización de APIs REST.
- **Pytest-HTML**: Generación automática de reportes de prueba en formato HTML.
- **Webdriver-Manager**: Gestión automática de drivers de navegador.

---

## 📂 Estructura de Directorios
```text
proyecto-final-automation-testing-cristian-purpura/
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline de integración continua (GitHub Actions)
├── data/
│   └── login_data.json         # Datasets parametrizados para pruebas de login
├── pages/
│   ├── base_page.py            # Clase base POM con wrappers de espera explícita
│   ├── login_page.py           # Page Object para autenticación
│   ├── inventory_page.py       # Page Object para inventario y carrito
│   └── checkout_page.py        # Page Object para pagos y envíos
├── tests/
│   ├── ui/
│   │   └── test_ecommerce_flow.py # Pruebas UI (Parametrizadas y E2E)
│   ├── api/
│   │   └── test_api_users.py      # Pruebas API REST (GET, POST, DELETE)
│   └── conftest.py             # Configuración global, fixtures y hooks de pytest
├── utils/
│   ├── api_client.py           # Cliente HTTP wrapper con logging
│   └── logger.py               # Configuración centralizada de logging (consola y archivo)
├── reports/                    # Reportes HTML generados automáticamente
├── screenshots/                # Capturas de pantalla capturadas ante fallos de UI
├── requirements.txt            # Dependencias del proyecto
└── pytest.ini                  # Configuración de pytest (marcadores y salida HTML)
```

---

## ⚙️ Instalación

1. Clonar el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd proyecto-final-automation-testing-cristian-purpura
   ```

2. Crear y activar un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/macOS:
   source venv/bin/activate
   ```

3. Instalar las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧪 Ejecución de Pruebas

El framework cuenta con marcadores personalizados configurados en `pytest.ini` para ejecutar suites específicas:

- **Ejecutar todas las pruebas (UI y API):**
  ```bash
  pytest
  ```

- **Ejecutar únicamente las pruebas de Interfaz de Usuario (UI):**
  ```bash
  pytest -m ui
  ```

- **Ejecutar únicamente las pruebas de API REST:**
  ```bash
  pytest -m api
  ```

---

## 📊 Reportes y Capturas de Pantalla Automáticas

- **Reportes HTML**: Al finalizar la ejecución de las pruebas, se genera automáticamente un reporte visual detallado en `reports/report.html`.
- **Captura Automática de Errores**: Mediante el hook `pytest_runtest_makereport` ubicado en `tests/conftest.py`, si una prueba de UI falla durante su ejecución, el framework toma automáticamente una captura de pantalla y la almacena en la carpeta `screenshots/` con marca de tiempo, facilitando la depuración y análisis de causa raíz.

### 🔍 Auditoría y Demostración en Vivo (`test_forced_failure_for_screenshot`)
La suite de pruebas incluye intencionalmente un test denominado `test_forced_failure_for_screenshot` que siempre fallará de forma controlada. El propósito profesional de este test es auditar y demostrar en vivo la funcionalidad del hook `pytest_runtest_makereport`, validando tanto la captura automática del estado visual ante fallos como su inyección directa en el reporte HTML.

---

## 🔄 Integración Continua (CI/CD)
El proyecto incluye un pipeline automatizado en GitHub Actions (`.github/workflows/ci.yml`) que se ejecuta en cada `push` o `pull_request` hacia la rama `main`. Este workflow:
1. Configura el entorno en Ubuntu con Python 3.10.
2. Instala todas las dependencias.
3. Ejecuta la suite completa de pruebas.
4. Almacena los reportes HTML generados como artefactos descargables (`test-reports`).
