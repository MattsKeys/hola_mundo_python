import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Asistente IA", layout="wide")

# 1. Inicialización del Estado de la Sesión (State Management)
if "historial_chat" not in st.session_state:
    st.session_state.historial_chat = [
        {"role": "assistant", "content": "Hola, ¿en qué puedo ayudarte?"}
    ]

if "cantidad_botones" not in st.session_state:
    st.session_state.cantidad_botones = 3  # Inicializamos con 3 para probar

# --- SECCIÓN 1: BOTONERA DINÁMICA ---
st.subheader("🛠️ Panel de Acciones")

# Creamos las 5 columnas requeridas
columnas = st.columns(5)

# Distribución de botones con desplegables (st.selectbox o st.menu)
for i in range(st.session_state.cantidad_botones):
    # El operador (%) distribuye los elementos entre las 5 columnas
    with columnas[i % 5]:
        st.selectbox(
            label=f"Grupo {i+1}",
            options=[f"Acción A {i+1}", f"Acción B {i+1}"],
            key=f"combo_{i}",
        )

st.divider()

# --- SECCIÓN 2: INTERFAZ DE CHAT ---
st.subheader("💬 Historial de Conversación")

# Contenedor para el "ida y vuelta"
contenedor_chat = st.container(height=400)

with contenedor_chat:
    for mensaje in st.session_state.historial_chat:
        with st.chat_message(mensaje["role"]):
            st.write(mensaje["content"])

# Entrada de texto y botón de envío (Streamlit lo integra nativamente en un componente)
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Insertar el mensaje del usuario en la pantalla
    with contenedor_chat.chat_message("user"):
        st.write(prompt)
    # Guardar en el historial
    st.session_state.historial_chat.append({"role": "user", "content": prompt})

    # Aquí se conectará la lógica de IA más adelante
    respuesta_ia = f"Recibí tu entrada: '{prompt}'. Procesando..."

    with contenedor_chat.chat_message("assistant"):
        st.write(respuesta_ia)
    st.session_state.historial_chat.append(
        {"role": "assistant", "content": respuesta_ia}
    )