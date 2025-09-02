import json
import polyline
import matplotlib.pyplot as plt
import io
import pandas as pd
import math


def create_latest_activity_poster(df):
    """
    Crée une affiche minimaliste (statique) de la dernière activité.

    Args:
        df (pd.DataFrame): DataFrame contenant au minimum :
                           - 'map' (dict ou JSON string avec 'summary_polyline')
                           - 'sport_type' (str)
                           - 'start_date' (datetime)
                           - 'distance' (float, en km)
                           - 'elapsed_time_hms' (formatée)
        save_path (str): chemin d'export de l'image finale (PNG).
    """

    plt.rcParams["figure.dpi"] = 300   # rendu à l'écran

    if df.empty:
        print("Df empty")
        return None

    # Trier par date décroissante
    df_sorted = df.sort_values('start_date', ascending=False)
    latest_activity = df_sorted.iloc[0]

    latest_activity_date = latest_activity["start_date"]
    latest_activity_date = pd.to_datetime(latest_activity_date)
    latest_activity_date_str = latest_activity_date.strftime("%d/%m/%Y")


    # Charger map
    map_data = latest_activity['map']
    if isinstance(map_data, str):
        try:
            map_data = json.loads(map_data)
        except Exception as e:
            print(f"Erreur JSON dans map : {e}")
            return None

    # Extraire polyline
    polyline_str = map_data.get("summary_polyline")
    if not polyline_str:
        print("Pas de polyline disponible.")
        return None

    coords = polyline.decode(polyline_str)
    lats, lons = zip(*coords)

    # Distance, temps et d+
    distance = latest_activity.get("distance", None)
    elapsed_time = latest_activity.get("elapsed_time_hms", None)
    dplus = latest_activity.get("total_elevation_gain", None)


    # --- 🎨 Création affiche ---
    fig, ax = plt.subplots(figsize=(8, 10))

    # Trace minimaliste
    ax.plot(lons, lats, color="white", linewidth=2)

    # Supprimer axes
    ax.set_axis_off()
    ax.set_facecolor("black")
    fig.patch.set_facecolor('black')


    # Nom de l'activité en haut
    fig.text(
        0.5, 0.95,              # 95% de la hauteur de la figure
        latest_activity["name"], # nom de l'activité
        ha="center",
        va="top",
        color="white",
        fontsize=20,
        family="monospace"
    )

    # Ajouter les datas principales
    if distance and elapsed_time and dplus:
        fig.text(
            0.5, -0.05,
            f"{distance:.1f} km | {elapsed_time} | {dplus:.0f} m D+",
            ha="center", va="top",
            color="white", fontsize=16, family="monospace"
        )

    # Date en dessous
    if latest_activity_date_str :
        fig.text(
            0.5, 0.015,  # légèrement plus bas
            latest_activity_date_str,    # formatée en "JJ/MM/AAAA"
            ha="center",
            va="bottom",
            color="white",
            fontsize=9,  # plus petite
            family="monospace"
        )


    return fig




def plot_mini_maps_grid(df):

    plt.rcParams["figure.dpi"] = 300   # rendu à l'écran

    # --- Filtrage sur 2025 et Run/Trail ---
    df_filtered = df[
        (pd.to_datetime(df["start_date"]).dt.year == 2025) &
        (df["sport_type"].isin(["Run", "Trail"]))
    ].copy()

    # --- Supprimer activités sans map ou polyline ---
    df_filtered = df_filtered[
        df_filtered["map"].apply(lambda x: bool(json.loads(x).get("summary_polyline")))
    ]

    # Trier du plus ancien au plus récent
    df_filtered = df_filtered.sort_values("start_date", ascending=True)

    n = len(df_filtered)
    if n == 0:
        print("Aucune activité Run ou Trail en 2025 avec polyline")
        return None

    # --- Calcul grille dynamique ---
    n_cols = math.ceil(math.sqrt(n))
    n_rows = math.ceil(n / n_cols)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols, n_rows), gridspec_kw={"wspace": 0.5, "hspace": 0.5})
    axes = axes.flatten()

    for i, (_, activity) in enumerate(df_filtered.iterrows()):
        try:
            map_json = json.loads(activity["map"])
            polyline_str = map_json.get("summary_polyline")
            coords = polyline.decode(polyline_str)
            lats, lons = zip(*coords)

            axes[i].plot(lons, lats, color="black", linewidth=0.3)
            axes[i].axis("off")
            axes[i].set_aspect("equal")
        except Exception as e:
            print(f"Erreur activité {activity['activity_id']}: {e}")

    # Cases vides (si grille > n)
    for j in range(i+1, len(axes)):
        axes[j].axis("off")

    return fig
