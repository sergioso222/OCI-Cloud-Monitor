# OCI-Cloud-Monitor

Aplicación web ligera desarrollada con **Python (Flask)** y el **SDK oficial de Oracle Cloud Infrastructure (OCI)** para consultar y monitorear en tiempo real el estado e información de red de instancias de cómputo (*Compute Instances*) dentro de un compartimento.

## Características
- **Autenticación segura con OCI API Key:** Firma criptográfica de peticiones gestionada mediante el SDK oficial de Oracle y variables de entorno.
- **Consulta de infraestructura en tiempo real:** Obtiene el nombre de la instancia, *shape*, estado del ciclo de vida (`RUNNING`, `STOPPED`, etc.), región, fecha de creación e interfaces de red (IP pública y privada).
- **Interfaz responsiva:** Dashboard construido con HTML5, JavaScript (Fetch API) y Tailwind CSS.

## Tecnologías utilizadas
- **Backend:** Python 3, Flask, OCI Python SDK, Python-Dotenv
- **Frontend:** HTML5, JavaScript (ES6+), Tailwind CSS

## Requisitos previos
- Python 3.9 o superior instalado.
- Cuenta de Oracle Cloud Infrastructure (OCI) con una **API Key** generada (llave privada `.pem`, *User OCID*, *Tenancy OCID*, *Fingerprint* y *Compartment OCID*).

## Instalación y ejecución local

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/sergioso222/OCI-Cloud-Monitor.git](https://github.com/sergioso222/OCI-Cloud-Monitor.git)
   cd OCI-Cloud-Monitor

2. **Crear y activar el entorno virtual:**
    - python -m venv venv
    ### En Windows (PowerShell):
    - .\venv\Scripts\activate
    ### En Linux / macOS:
    - source venv/bin/activate

3. **Instalar las dependencias:**
    - pip install -r requirements.txt

4. **Configurar las variables de entorno:**
    ### En Windows (PowerShell):
    - Copy-Item .env.example .env
    ### En Linux / macOS:
    - cp .env.example .env

5. **Ejecutar la aplicacion:**
    - python app.py
