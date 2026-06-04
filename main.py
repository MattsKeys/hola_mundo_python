import cowsay
import sys

from transacciones import ejecutar_proceso
from src.ejercicios.funciones_basicas_M import Prueba
import src.ejercicios.funciones_basicas


def menu_principal():
    print("bienvenides")
    print("=== SISTEMA SELECTOR DE EJERCICIOS ===")
    print("1. Ejecutar procesamiento de transacciones")
    print("2. Mostrar mensajes de cowsay")
    print("3. Enviar Prompt")
    #print("3/. Enviar Prompt")
    print("x. Salir")
    
    opcion = input("Seleccione una opción: ")

    match opcion:
        case "1":
            ejecutar_proceso()
        case "2":
            cowsay_mensajes()
        case "3":
            src.ejercicios.funciones_basicas.main()
        case "5":
            Prueba() 
        case "x":
            print("Cerra el orto.")
        case _:
            print("¿Sos pelotudo?")
        

def cowsay_mensajes():
    cowsay.cow("vaca")
    cowsay.fox("zorro")
<<<<<<< HEAD
    cowsay.tux("linux")
    cowsay.ghostbusters("cazafantasmas")
=======
    cowsay.daemon("demonio")

>>>>>>> 06c2dd384e04dc3a4a3e6788c42ad3c817566987

if __name__ == "__main__":
    menu_principal()

