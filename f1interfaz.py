import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import shutil
import atexit
from matplotlib.collections import LineCollection
from datetime import date
import streamlit as st

# ── Rutas ──────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
cache_path  = os.path.join(BASE_DIR, "f1_cache")
output_path = os.path.join(BASE_DIR, "f1_cache", "graficos")

os.makedirs(cache_path,  exist_ok=True)
os.makedirs(output_path, exist_ok=True)
fastf1.Cache.enable_cache(cache_path)

# ── Limpieza al cerrar ─────────────────────────────────────────────────────
def limpiar_todo():
    shutil.rmtree(cache_path,  ignore_errors=True)
    os.makedirs(cache_path,  exist_ok=True)

atexit.register(limpiar_todo)  # se ejecuta al cerrar el proceso

# ── UI ────────────────────────────────────────────────────────────────────
st.title("🏎️ Gráficos F1")

anio    = st.number_input("Año", min_value=2018, max_value=date.today().year, value=date.today().year)
circuito = st.text_input("Circuito (ej: Monaco, Bahrain, Canada)")

grafico = st.selectbox("Gráfico", [
    "1. Tiempos de vuelta (Clasificación)",
    "2. Telemetría comparada",
    "3. Mapa de velocidad",
    "4. Estrategia de neumáticos",
    "5. Evolución de posiciones",
])

# Inputs extra según gráfico
driver1 = driver2 = None
if grafico in ("2. Telemetría comparada", "3. Mapa de velocidad"):
    driver1 = st.text_input("Piloto 1 (ej: LEC, VER, HAM)")
if grafico == "2. Telemetría comparada":
    driver2 = st.text_input("Piloto 2 (ej: LEC, VER, HAM)")

generar = st.button("Generar gráfico")

# ── Funciones ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Cargando sesión...")
def cargar_sesion(anio, circuito, tipo, telemetria=False):
    session = fastf1.get_session(anio, circuito, tipo)
    session.load(laps=True, telemetry=telemetria, weather=False)
    return session


def grafico_tiempos_vuelta(anio, circuito):
    session = cargar_sesion(anio, circuito, "Q")
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme="fastf1")

    laps = session.laps.pick_quicklaps().reset_index(drop=True)
    laps["LapTime_s"] = laps["LapTime"].dt.total_seconds()
    order = laps.groupby("Driver")["LapTime_s"].min().sort_values().index.tolist()

    fig, ax = plt.subplots(figsize=(14, 6))
    for i, driver in enumerate(order):
        driver_laps = laps[laps["Driver"] == driver]["LapTime_s"]
        color = fastf1.plotting.get_driver_color(driver, session)
        ax.boxplot(driver_laps, positions=[i], widths=0.4, patch_artist=True,
                   boxprops=dict(facecolor=color, alpha=0.8),
                   medianprops=dict(color="white", linewidth=2),
                   whiskerprops=dict(color=color), capprops=dict(color=color),
                   flierprops=dict(marker="o", color=color, alpha=0.4, markersize=4))

    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, rotation=45, ha="right")
    ax.set_ylabel("Tiempo de vuelta (s)")
    ax.set_title(f"{circuito} {anio} – Q: Distribución de tiempos de vuelta", fontsize=14)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    return fig


def grafico_telemetria_comparada(anio, circuito, driver1, driver2):
    session = cargar_sesion(anio, circuito, "Q", telemetria=True)
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme="fastf1")

    lap1 = session.laps.pick_driver(driver1).pick_fastest()
    lap2 = session.laps.pick_driver(driver2).pick_fastest()
    tel1 = lap1.get_car_data().add_distance()
    tel2 = lap2.get_car_data().add_distance()
    color1 = fastf1.plotting.get_driver_color(driver1, session)
    color2 = fastf1.plotting.get_driver_color(driver2, session)

    fig, axes = plt.subplots(3, 1, figsize=(13, 9), sharex=True)
    fig.suptitle(f"{circuito} {anio} – Q: {driver1} vs {driver2}", fontsize=14)

    axes[0].plot(tel1["Distance"], tel1["Speed"],            color=color1, label=driver1)
    axes[0].plot(tel2["Distance"], tel2["Speed"],            color=color2, label=driver2, linestyle="--")
    axes[0].set_ylabel("Velocidad (km/h)"); axes[0].legend(); axes[0].grid(alpha=0.3)

    axes[1].plot(tel1["Distance"], tel1["Throttle"],         color=color1, label=driver1)
    axes[1].plot(tel2["Distance"], tel2["Throttle"],         color=color2, label=driver2, linestyle="--")
    axes[1].set_ylabel("Acelerador (%)"); axes[1].grid(alpha=0.3)

    axes[2].plot(tel1["Distance"], tel1["Brake"].astype(int),        color=color1, label=driver1)
    axes[2].plot(tel2["Distance"], tel2["Brake"].astype(int) * 0.85, color=color2, label=driver2, linestyle="--")
    axes[2].set_ylabel("Freno"); axes[2].set_xlabel("Distancia (m)"); axes[2].grid(alpha=0.3)

    plt.tight_layout()
    return fig


def grafico_mapa_velocidad(anio, circuito, driver1):
    session = cargar_sesion(anio, circuito, "Q", telemetria=True)
    lap = session.laps.pick_driver(driver1).pick_fastest()
    pos = lap.get_pos_data()
    tel = lap.get_car_data().add_distance()

    merged = tel[["Distance", "Speed"]].copy()
    pos = pos.copy()
    pos["Distance"] = np.linspace(0, merged["Distance"].max(), len(pos))
    pos["Speed"]    = np.interp(pos["Distance"], merged["Distance"], merged["Speed"])

    x, y, speed = pos["X"].values, pos["Y"].values, pos["Speed"].values
    points   = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fig, ax = plt.subplots(figsize=(10, 8))
    norm = plt.Normalize(speed.min(), speed.max())
    lc   = LineCollection(segments, cmap="RdYlGn", norm=norm, linewidth=3)
    lc.set_array(speed)
    ax.add_collection(lc)
    fig.colorbar(lc, ax=ax).set_label("Velocidad (km/h)")
    ax.set_xlim(x.min() - 100, x.max() + 100)
    ax.set_ylim(y.min() - 100, y.max() + 100)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"{circuito} {anio} – Q: Mapa de velocidad — {driver1}", fontsize=14)
    plt.tight_layout()
    return fig


def grafico_estrategia_neumaticos(anio, circuito):
    session = cargar_sesion(anio, circuito, "R")
    laps    = session.laps[["Driver", "LapNumber", "Compound", "TyreLife"]].dropna()
    compound_colors = {
        "SOFT": "#E8002D", "MEDIUM": "#FFF200", "HARD": "#EBEBEB",
        "INTERMEDIATE": "#39B54A", "WET": "#0067FF", "UNKNOWN": "#999999",
    }
    drivers_sorted = sorted(laps["Driver"].unique())

    fig, ax = plt.subplots(figsize=(14, 9))
    for i, driver in enumerate(drivers_sorted):
        for _, lap in laps[laps["Driver"] == driver].sort_values("LapNumber").iterrows():
            compound = lap["Compound"] if lap["Compound"] in compound_colors else "UNKNOWN"
            ax.barh(i, width=1, left=lap["LapNumber"] - 1,
                    color=compound_colors[compound], edgecolor="none", height=0.8)

    ax.set_yticks(range(len(drivers_sorted)))
    ax.set_yticklabels(drivers_sorted, fontsize=8)
    ax.set_xlabel("Vuelta")
    ax.set_title(f"{circuito} {anio} – Carrera: Estrategia de neumáticos", fontsize=14)
    ax.legend(handles=[mpatches.Patch(color=v, label=k)
                        for k, v in compound_colors.items() if k != "UNKNOWN"],
              loc="lower right", fontsize=9)
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    return fig


def grafico_posiciones_carrera(anio, circuito):
    session = cargar_sesion(anio, circuito, "R")
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme="fastf1")

    laps = session.laps[["Driver", "LapNumber", "Position"]].dropna()
    laps["Position"] = laps["Position"].astype(int)

    fig, ax = plt.subplots(figsize=(14, 8))
    for driver in laps["Driver"].unique():
        d     = laps[laps["Driver"] == driver].sort_values("LapNumber")
        color = fastf1.plotting.get_driver_color(driver, session)
        ax.plot(d["LapNumber"], d["Position"], color=color, linewidth=1.5, label=driver)
        last  = d.iloc[-1]
        ax.text(last["LapNumber"] + 0.3, last["Position"], driver,
                fontsize=7, color=color, va="center")

    ax.set_ylim(20.5, 0.5); ax.set_yticks(range(1, 21))
    ax.set_xlabel("Vuelta"); ax.set_ylabel("Posición")
    ax.set_title(f"{circuito} {anio} – Carrera: Evolución de posiciones", fontsize=14)
    ax.grid(alpha=0.2)
    plt.tight_layout()
    return fig


# ── Renderizado ───────────────────────────────────────────────────────────
if generar:
    if not circuito:
        st.warning("Ingresá el nombre del circuito.")
    else:
        try:
            with st.spinner("Generando gráfico..."):
                match grafico:
                    case "1. Tiempos de vuelta (Clasificación)":
                        fig = grafico_tiempos_vuelta(anio, circuito)
                    case "2. Telemetría comparada":
                        fig = grafico_telemetria_comparada(anio, circuito, driver1, driver2)
                    case "3. Mapa de velocidad":
                        fig = grafico_mapa_velocidad(anio, circuito, driver1)
                    case "4. Estrategia de neumáticos":
                        fig = grafico_estrategia_neumaticos(anio, circuito)
                    case "5. Evolución de posiciones":
                        fig = grafico_posiciones_carrera(anio, circuito)

            st.pyplot(fig)
            plt.close(fig)

        except KeyboardInterrupt:
            limpiar_todo()
        except Exception as e:
            st.error(f"Error: {e}\nVerificá el año, circuito y piloto.")