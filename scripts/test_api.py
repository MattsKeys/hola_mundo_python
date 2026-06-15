import httpx
from pydantic_settings import BaseSettings

class ClienteSettings(BaseSettings):
    api_mayuscula_url: str

    class Config:
        env_file = ".env"
        case_sensitive = False

cliente_settings = ClienteSettings()

def ejecutar_cliente():
    print("=========================================")
    print("  💻 INTERFAZ DE CONSUMO DE LA API")
    print("=========================================\n")
    
    # 2. Captura de datos interactiva
    usuario = input("👤 Ingrese usuario: ").strip()
    contrasenia = input("🔑 Ingrese contraseña: ").strip()
    texto_original = input("📝 Ingrese el texto a procesar: ").strip()

    # 3. Construcción del Payload (Debe respetar las llaves de PayloadInput)
    payload = {
        "usuario": usuario,
        "contrasenia": contrasenia,
        "texto": texto_original
    }

    # 4. Envío de la petición HTTP POST
    url_final = f"{cliente_settings.api_mayuscula_url}/procesar"
    
    try:
        # Realizamos la petición de forma síncrona para este script de consola
        response = httpx.post(url_final, json=payload)
        
        # 5. Manejo del protocolo de respuestas HTTP
        if response.status_code == 200:
            resultado = response.json()
            print("\n✅ [Servidor 200 OK] Procesamiento Exitoso:")
            print(f"👉 Resultado: {resultado}")
            
        elif response.status_code == 401:
            print("\n❌ [Servidor 401 Unauthorized] Error de Seguridad:")
            print(f"👉 Detalle: {response.json().get('detail')}")
            
        elif response.status_code == 422:
            print("\n🚨 [Servidor 422 Unprocessable Entity] Error de Validación:")
            print("👉 Pydantic rechazó los datos. Asegúrese de no enviar campos vacíos.")
            
        else:
            print(f"\n❓ Código inesperado ({response.status_code}): {response.text}")
            
    except httpx.ConnectError:
        print("\n🚨 Error de red: No se pudo establecer conexión con la API.")
        print(f"Compruebe que Uvicorn esté encendido en: {cliente_settings.api_mayuscula_url}")

if __name__ == "__main__":
    ejecutar_cliente()