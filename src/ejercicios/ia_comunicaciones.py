from src.ejercicios.ia_diccionario import ConfigIA

def simula_envio(configuracion_ia: ConfigIA) -> str:
    prompt = f"Usaste el modelo {configuracion_ia["modelo"]} y generaste este prompt: Eres un experto en {configuracion_ia["tema"]}: {configuracion_ia["consulta"]}"
    return prompt
    