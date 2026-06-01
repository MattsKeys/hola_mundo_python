import cowsay

from transacciones import ejecutar_proceso


def menu_principal():
    print("=== SISTEMA SELECTOR DE EJERCICIOS ===")
    print("1. Ejecutar procesamiento de transacciones")
    print("2. Mostrar mensajes de cowsay")
    print("3. Pendiente programar")
    print("x. Salir")
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == "1":
        ejecutar_proceso()
    elif opcion == "2":
        cowsay_mensajes()
    elif opcion == "3":
        print("Opcion pendiente de programar")
    elif opcion == "x":
        print("Cerra el orto.")
    else:
        print("Opción no válida.")


def cowsay_mensajes():
    cowsay.cow("vaca")
    cowsay.fox("zorro")


if __name__ == "__main__":
    menu_principal()

