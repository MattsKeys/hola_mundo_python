def ejecutar_proceso():
    """
    Función principal que orquesta el filtrado de transacciones.
    (Aquí irá la resolución del desafío anterior)
    """

    transacciones = [
        {"id": 101, "tipo": "ingreso", "monto": 15000},
        {"id": 102, "tipo": "egreso", "monto": 3500},
        {"id": 103, "tipo": "ingreso", "monto": 8000},
        {"id": 104, "tipo": "ingreso", "monto": 22000},
    ]

    total_impuestos = 0

    for transaccion in transacciones:
        if transaccion["tipo"] == "ingreso" and transaccion["monto"] > 10000:
            impuesto = transaccion["monto"] * 0.02
            total_impuestos += impuesto
            print(f"Transacción ID: {transaccion['id']}, Impuesto a pagar: {impuesto:.2f}")
  
    print(f"Total de impuestos a pagar: {total_impuestos:.2f}")

