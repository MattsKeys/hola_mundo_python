import cowsay
import sys

from transacciones import ejecutar_proceso
#from src.ejercicios.ia_diccionario import ConfigIA,init_config_ia
#from src.ejercicios.ia_comunicaciones import simula_envio
import src.ejercicios.funciones_basicas


def menu_principal():
    print("bienvenides")
    print("=== SISTEMA SELECTOR DE EJERCICIOS ===")
    print("1. Ejecutar procesamiento de transacciones")
    print("2. Mostrar mensajes de cowsay")
    print("3. Enviar Prompt")
    print("4. ponete en 4")
    print("x. Salir")
    
    opcion = input("Seleccione una opción: ")

    match opcion:
        case "1":
            ejecutar_proceso()
        case "2":
            cowsay_mensajes()
        case "3":

            #configuracion_ia: ConfigIA = init_ConfigIA()
            #configuracion_ia["modelo"] = input("Seleccione modelo:")
            #configuracion_ia["tema"] = input("Seleccione tema:")
            #configuracion_ia["consulta"] = input("Seleccione consulta:")

            #respuesta = simula_envio(configuracion_ia)
            #print(f"Esta es la respuesta de la funcion: {respuesta}")
        case "5":
            Prueba()
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

