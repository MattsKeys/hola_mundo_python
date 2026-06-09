import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import os
from matplotlib.collections import LineCollection

# Crea la carpeta si no existe, luego activa el caché
cache_path = os.path.join(os.path.dirname(__file__), "f1_cache")
os.makedirs(cache_path, exist_ok=True)
fastf1.Cache.enable_cache(cache_path)


# 1. COMPARACIÓN DE TIEMPOS DE VUELTA — todos los pilotos en clasificación
# 
def grafico_tiempos_vuelta():
    """Boxplot con la distribución de tiempos de vuelta por piloto."""
    
    anio: int = int(input("  Año (ej: 2024): ").strip())
    circuito = input("  Circuito (ej: Monaco, Bahrain, Canada): ").strip()

    session = fastf1.get_session(anio, circuito, "Q")
    session.load(laps=True, telemetry=False, weather=False)

    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme="fastf1")

    # Solo vueltas rápidas válidas (sin pit in/out)
    laps = session.laps.pick_quicklaps().reset_index(drop=True)
    laps["LapTime_s"] = laps["LapTime"].dt.total_seconds()

    # Ordenar pilotos por su mejor vuelta
    order = (
        laps.groupby("Driver")["LapTime_s"]
        .min()
        .sort_values()
        .index.tolist()
    )

    fig, ax = plt.subplots(figsize=(14, 6))

    for i, driver in enumerate(order):
        driver_laps = laps[laps["Driver"] == driver]["LapTime_s"]
        color = fastf1.plotting.get_driver_color(driver, session)
        ax.boxplot(
            driver_laps,
            positions=[i],
            widths=0.4,
            patch_artist=True,
            boxprops=dict(facecolor=color, alpha=0.8),
            medianprops=dict(color="white", linewidth=2),
            whiskerprops=dict(color=color),
            capprops=dict(color=color),
            flierprops=dict(marker="o", color=color, alpha=0.4, markersize=4),
        )

    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, rotation=45, ha="right")
    ax.set_ylabel("Tiempo de vuelta (s)")
    ax.set_title("Canada 2026 – Q: Distribución de tiempos de vuelta", fontsize=14)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig("1_tiempos_vuelta_Canada_Q.png", dpi=150)
    plt.show()
    print("✅ Gráfico 1 guardado.")

# 2. TELEMETRÍA COMPARADA — velocidad de dos pilotos en la vuelta rápida
# 

def grafico_telemetria_comparada(driver1, driver2):
    """
    Compara velocidad, acelerador y freno de dos pilotos
    a lo largo de una vuelta en clasificación.
    """
    anio: int = int(input("  Año (ej: 2024): ").strip())
    circuito = input("  Circuito (ej: Monaco, Bahrain, Canada): ").strip()
    
    session = fastf1.get_session(anio, circuito, "Q")
    session.load(laps=True, telemetry=True, weather=False)

    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme="fastf1")

    lap1 = session.laps.pick_driver(driver1).pick_fastest()
    lap2 = session.laps.pick_driver(driver2).pick_fastest()

    tel1 = lap1.get_car_data().add_distance()
    tel2 = lap2.get_car_data().add_distance()

    color1 = fastf1.plotting.get_driver_color(driver1, session)
    color2 = fastf1.plotting.get_driver_color(driver2, session)

    fig, axes = plt.subplots(3, 1, figsize=(13, 9), sharex=True)
    fig.suptitle(
        f"Canada 2026 – Q: {driver1} vs {driver2} (vuelta rápida)", fontsize=14
    )

    # Velocidad
    axes[0].plot(tel1["Distance"], tel1["Speed"], color=color1, label=driver1)
    axes[0].plot(tel2["Distance"], tel2["Speed"], color=color2, label=driver2, linestyle="--")
    axes[0].set_ylabel("Velocidad (km/h)")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    # Acelerador (%)
    axes[1].plot(tel1["Distance"], tel1["Throttle"], color=color1, label=driver1)
    axes[1].plot(tel2["Distance"], tel2["Throttle"], color=color2, label=driver2, linestyle="--")
    axes[1].set_ylabel("Acelerador (%)")
    axes[1].grid(alpha=0.3)

    # Freno (booleano → 0/1)
    axes[2].plot(tel1["Distance"], tel1["Brake"].astype(int), color=color1, label=driver1)
    axes[2].plot(tel2["Distance"], tel2["Brake"].astype(int) * 0.85, color=color2, label=driver2, linestyle="--")
    axes[2].set_ylabel("Freno")
    axes[2].set_xlabel("Distancia (m)")
    axes[2].grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("2_telemetria_comparada_Canada_Q.png", dpi=150)
    plt.show()
    print("✅ Gráfico 2 guardado.")

 # 3. MAPA DEL CIRCUITO coloreado por velocidad
# 
    
def grafico_mapa_velocidad(driver1):
    """Dibuja el trazado del circuito coloreado según la velocidad del piloto."""
    
    anio: int = int(input("  Año (ej: 2024): ").strip())
    circuito = input("  Circuito (ej: Monaco, Bahrain, Canada): ").strip()
 
    session = fastf1.get_session(anio, circuito, "Q")
    session.load(laps=True, telemetry=True, weather=False)
 
    lap = session.laps.pick_driver(driver1).pick_fastest()
    pos = lap.get_pos_data()
    tel = lap.get_car_data().add_distance()
 
    # Interpolar velocidad en los puntos de posición
    merged = tel[["Distance", "Speed"]].copy()
    pos = pos.copy()
    pos["Distance"] = np.linspace(0, merged["Distance"].max(), len(pos))
    pos["Speed"] = np.interp(pos["Distance"], merged["Distance"], merged["Speed"])
 
    x = pos["X"].values
    y = pos["Y"].values
    speed = pos["Speed"].values
 
    # Crear segmentos para LineCollection
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
 
    fig, ax = plt.subplots(figsize=(10, 8))
    norm = plt.Normalize(speed.min(), speed.max())
    lc = LineCollection(segments, cmap="RdYlGn", norm=norm, linewidth=3)
    lc.set_array(speed)
    ax.add_collection(lc)
 
    cbar = fig.colorbar(lc, ax=ax)
    cbar.set_label("Velocidad (km/h)")
 
    ax.set_xlim(x.min() - 100, x.max() + 100)
    ax.set_ylim(y.min() - 100, y.max() + 100)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"Canada 2026 – Q: Mapa de velocidad — {driver1}", fontsize=14)
 
    plt.tight_layout()
    plt.savefig("3_mapa_velocidad_Canada.png", dpi=150)
    plt.show()
    print("✅ Gráfico 3 guardado.")

# 4. ESTRATEGIA DE NEUMÁTICOS — carrera completa
# 

def grafico_estrategia_neumaticos():
    """
    Visualiza los compuestos y el stint de neumáticos
    de cada piloto durante la carrera.
    """
    anio: int = int(input("  Año (ej: 2024): ").strip())
    circuito = input("  Circuito (ej: Monaco, Bahrain, Canada): ").strip()

    session = fastf1.get_session(anio, circuito, "R")
    session.load(laps=True, telemetry=False, weather=False)

    laps = session.laps[["Driver", "LapNumber", "Compound", "TyreLife"]].dropna()

    compound_colors = {
        "SOFT": "#E8002D",
        "MEDIUM": "#FFF200",
        "HARD": "#EBEBEB",
        "INTERMEDIATE": "#39B54A",
        "WET": "#0067FF",
        "UNKNOWN": "#999999",
    }

    drivers = laps["Driver"].unique()
    drivers_sorted = sorted(drivers)

    fig, ax = plt.subplots(figsize=(14, 9))

    for i, driver in enumerate(drivers_sorted):
        driver_laps = laps[laps["Driver"] == driver].sort_values("LapNumber")
        for _, lap in driver_laps.iterrows():
            compound = lap["Compound"] if lap["Compound"] in compound_colors else "UNKNOWN"
            color = compound_colors[compound]
            ax.barh(
                i,
                width=1,
                left=lap["LapNumber"] - 1,
                color=color,
                edgecolor="none",
                height=0.8,
            )

    ax.set_yticks(range(len(drivers_sorted)))
    ax.set_yticklabels(drivers_sorted, fontsize=8)
    ax.set_xlabel("Vuelta")
    ax.set_title("Miami 2026 – Carrera: Estrategia de neumáticos", fontsize=14)

    # Leyenda
    patches = [
        mpatches.Patch(color=v, label=k) for k, v in compound_colors.items() if k != "UNKNOWN"
    ]
    ax.legend(handles=patches, loc="lower right", fontsize=9)
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    plt.savefig("4_estrategia_neumaticos_miami_R.png", dpi=150)
    plt.show()
    print("✅ Gráfico 4 guardado.")


# 5. EVOLUCIÓN DE POSICIONES — carrera
# 

def grafico_posiciones_carrera():
    """Muestra cómo cambian las posiciones de los pilotos vuelta a vuelta."""

    anio: int = int(input("  Año (ej: 2024): ").strip())
    circuito = input("  Circuito (ej: Monaco, Bahrain, Canada): ").strip()
    
    session = fastf1.get_session(anio, circuito, "R")
    session.load(laps=True, telemetry=False, weather=False)

    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme="fastf1")

    laps = session.laps[["Driver", "LapNumber", "Position"]].dropna()
    laps["Position"] = laps["Position"].astype(int)

    fig, ax = plt.subplots(figsize=(14, 8))

    for driver in laps["Driver"].unique():
        d = laps[laps["Driver"] == driver].sort_values("LapNumber")
        color = fastf1.plotting.get_driver_color(driver, session)
        ax.plot(d["LapNumber"], d["Position"], color=color, linewidth=1.5, label=driver)
        # Etiqueta al final de la línea
        last = d.iloc[-1]
        ax.text(last["LapNumber"] + 0.3, last["Position"], driver, fontsize=7, color=color, va="center")

    ax.set_ylim(20.5, 0.5)
    ax.set_yticks(range(1, 21))
    ax.set_xlabel("Vuelta")
    ax.set_ylabel("Posición")
    ax.set_title("Canada 2026 – Carrera: Evolución de posiciones", fontsize=14)
    ax.grid(alpha=0.2)

    plt.tight_layout()
    plt.savefig("5_posiciones_carrera_Canada.png", dpi=150)
    plt.show()
    print("✅ Gráfico 5 guardado.")


# MAIN — ejecutar todos los gráficos
# 

def menu_principal():
    while True:
        print("Gráficos F1\n")
        print("Seleccione una opción:\n")
        print("1. Tiempos de vuelta")
        print("2. Telemetría comparada")
        print("3. Mapa del circuito coloreado por velocidad")
        print("4. Estrategia de neumáticos")
        print("5. Evolución de posiciones en carrera")
        print("x. Salir")
    
  
        opcion = input("  Seleccioná una opción: ").strip().lower()

        try:
            match opcion:
                case "1":
                    grafico_tiempos_vuelta()
                case "2":
                    driver1 = input("  Piloto 1 (ej: COL, GAS, LEC): ").strip()
                    driver2 = input("  Piloto 2 (ej: COL, GAS, LEC): ").strip()
                    grafico_telemetria_comparada(driver1, driver2)
                case "3":
                    driver1 = input("  Piloto 1 (ej: COL, GAS, LEC): ").strip()
                    grafico_mapa_velocidad(driver1)
                case "4":
                    grafico_estrategia_neumaticos()
                case "5":
                    grafico_posiciones_carrera()
                case "x":
                    print("\n¡Hasta la próxima! 🏁\n")
                    break
                case _:
                    print("\n  ⚠️  Opción no válida, intentá de nuevo.")
                    
        except Exception as e:
            print(f"\n  Error: {e}")
            print("  Verificá el año y el nombre del circuito e intentá de nuevo.")
            
if __name__ == "__main__":
    menu_principal()