import cowsay
import sys
import src.ejercicios.funciones_basicas

from transacciones import ejecutar_proceso
from config.openvergai.chat import preguntar
#from config.openvergai.chat import preguntar

#from src.ejercicios.ia_diccionario import ConfigIA,init_config_ia
#from src.ejercicios.ia_comunicaciones import simula_envio


def menu_principal():
    print("bienvenides")
    print("=== SISTEMA SELECTOR DE EJERCICIOS ===")
    print("1. Ejecutar procesamiento de transacciones")
    print("2. Mostrar mensajes de cowsay")
    print("3. Enviar Prompt")
    print("4. ponete en 4")
    print("5. SHAT HABLA")
    print("8. Botonera")
    print("x. Salir")
    
    opcion = input("Seleccione una opción: ")

    match opcion:
        case "1":
            ejecutar_proceso()
        case "2":
            cowsay_mensajes()
        case "3":
            pass
            #configuracion_ia: ConfigIA = init_ConfigIA()
            #configuracion_ia["modelo"] = input("Seleccione modelo:")
            #configuracion_ia["tema"] = input("Seleccione tema:")
            #configuracion_ia["consulta"] = input("Seleccione consulta:")

            #respuesta = simula_envio(configuracion_ia)
            #print(f"Esta es la respuesta de la funcion: {respuesta}")
        case "5":
            print("Bienvenido al shat")

            prompt = input("Ingrese un prompt: ")
            
            match len(prompt):
                case 0:
                    print("comeme los eggs")
                
                case _:
                    respuesta = preguntar(prompt)
                    print(respuesta)

        case "8":
            pass
        case "x":
            print("Cerra el orto.")
        case _:
            print("¿Sos pelotudo?")
        

def cowsay_mensajes():
    cowsay.cow("vaca")
    cowsay.fox("zorro")
    cowsay.tux("linux")
    cowsay.ghostbusters("cazafantasmas")
    cowsay.daemon("demonio")
    cowsay.milk("milk")


if __name__ == "__main__":
    menu_principal()

