def control_tokens(lista_tokens):
    
    for token in lista_tokens:
    
        if token >= 5000:
            mensaje = "Alerta: consumo critico"
        elif token >= 1000:
            mensaje = "Consumo moderado"
        else:
            mensaje = "Consumo óptimo"
        
        print(mensaje)


import random

def enviar_prompt(prompt):
    #ejecución de código

    api_rta = random.choice(["ok","error_valor","error_timeout"])

    if api_rta == "error_valor":
        raise ValueError("Error API key")
    elif api_rta == "error_timeout":
        raise TimeoutError("Error timeout")
    else:
        http_rta = random.choice([200,401,429,500,503])
        return http_rta


prompt = "hola chat"
try:
    http_rta = enviar_prompt(prompt)

    match http_rta:
        case 200:
            print("Solicitud exitosa. Procesando tokens...")
        case 401:
            print("Error de autenticación: API Key inválida.")
        case 429:
            print("Límite de cuota excedido. Reintentando en breve...")
        case 500|503:
            print("Error del servidor de IA.")
        case _:
            print(f"error inesperado {http_rta}")

except ValueError as error:
    print(f"Error de API Key: {error}")
except TimeoutError as error:
    print(f"Error de TimeoutError: {error}")

