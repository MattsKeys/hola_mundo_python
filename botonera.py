import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Asistente IA", layout="wide")

# 1. Inicialización del Estado de la Sesión (State Management)
if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = [
        {"role": "assistant", "content": "Hola, ¿en qué puedo ayudarte?"}
    ]

# Variable clave: guarda qué acción se está ejecutando actualmente
if "accion_activa" not in st.session_state:
    st.session_state.accion_activa = None



# --- SECCIÓN 1: BOTONERA DINÁMICA ---
st.subheader("🛠️ Panel de Acciones")

# Creamos las 5 columnas requeridas
columnas = st.columns(5)

# Distribución de botones con desplegables (st.selectbox o st.menu)

with columnas[0]:
    seleccion = st.selectbox(
        label="Quick Test",
        options=["Seleccionar...", "Mensajes cowsay", "Proceso Transacciones"],
        key="combo_quick_test",
    )

# Evaluamos si el usuario seleccionó una opción válida (distinta al placeholder)
    if seleccion == "Mensajes cowsay":
        # 1. Registrar la acción en el historial como si fuera el usuario
        st.session_state.historial_chat.append(
            {"role": "user", "content": f"Ejecutar: {seleccion}"}
        )

        # 2. Generar la respuesta lógica
        output_cowsay = " _________________\n< Hola Mundo Python >\n -----------------\n        \\   ^__^\n         \\  (oo)\\_______\n            (__)\\       )\\/\\\n                ||----w |\n                ||     ||"

        # 3. Registrar el output en el chat
        st.session_state.historial_chat.append(
            {"role": "assistant", "content": f"```\n{output_cowsay}\n```"}
        )

        # 4. CRUCIAL: Limpiar la selección del combo para que no se ejecute en bucle
        # Volvemos a setear el índice al valor 0 ("Seleccionar...") para la próxima recarga
        st.components.v1.html(
            """
            <script>
                // Forzar el reset visual no es estrictamente necesario si usamos st.rerun() 
                // pero manejar el estado interno evita la ejecución doble.
            </script>
            """,
            height=0,
        )
        
        # Forzar el refresco de Streamlit con los nuevos datos del historial
        st.rerun()

    elif seleccion == "Proceso Transacciones":
        # Aquí se configurará la lógica para la otra opción del combo
        pass

with columnas[1]:
    st.selectbox(
        label="Autitos",
        options=["Seleccionar...", "Tiempos de vuelta", "Telemetria comparada", "Mapa de velocidad", "Estrategia de neumaticos", "Evolucion de posiciones"],
        key="combo_autitos",
    )

with columnas[2]:
    st.selectbox(
        label="Oficina de Marcos",
        options=["Seleccionar...", "Memazos", "Que paja todo bldo", "No entendes la metadata"],
        key="combo_oficina_de_marcos",
    )

with columnas[3]:
    st.selectbox(
        label="MambortNet",
        options=["Seleccionar...", "Programa 1", "Programa 2", "Programa 3"],
        key="combo_mambortnet",
    )

with columnas[4]:
    st.selectbox(
        label="Chat IA",
        options=["Seleccionar...", "Chat GPT", "Gemini", "Claude", "Deepseek", "Grok"],
        key="combo_chat_ia",
    )


# --- SECCIÓN 2: INTERFAZ DE CHAT ---

# Contenedor para el "ida y vuelta"
contenedor_chat = st.container(height=400)

with contenedor_chat:
    for mensaje in st.session_state.historial_chat:
        with st.chat_message(mensaje["role"]):
            st.write(mensaje["content"])


# --- SECCIÓN 3: PROCESAMIENTO DEL INPUT DEL CHAT ---
if entrada_usuario := st.chat_input("Escribe aquí..."):
    
    # 1. Mostrar lo que escribió el usuario
    with contenedor_chat.chat_message("user"):
        st.write(entrada_usuario)
    st.session_state.historial_chat.append({"role": "user", "content": entrada_usuario})

    # 2. Evaluar el contexto: ¿Había una acción esperando este input?
    if st.session_state.accion_activa == "calcular_doble":
        # Validación típica de analista: asegurar tipo de dato
        try:
            numero = float(entrada_usuario)
            resultado = numero * 2
            respuesta = f"El doble de {numero} es: **{resultado}**"
        except ValueError:
            respuesta = f"❌ '{entrada_usuario}' no es un número válido. Acción cancelada."
        
        # Resetear el estado de la acción para permitir otras nuevas
        st.session_state.accion_activa = None

    else:
        # Chat genérico (si no había ningún botón presionado previamente)
        respuesta = f"Conversación general: Recibí '{entrada_usuario}'"

    # 3. Mostrar respuesta y guardar en el historial
    with contenedor_chat.chat_message("assistant"):
        st.write(respuesta)
    st.session_state.historial_chat.append({"role": "assistant", "content": respuesta})
    
    # Forzar refresco visual para mantener el orden
    st.rerun()

