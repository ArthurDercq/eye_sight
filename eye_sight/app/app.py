from eye_sight.create_database import *
from eye_sight.update_database import *
from eye_sight.params import *
import streamlit as st
from sqlalchemy import create_engine, text
from eye_sight.params import *
import altair as alt
from eye_sight.plots.plot_calendar_heat import plot_calendar
from eye_sight.plots.basic_plots import *
from eye_sight.plots.plot_map import *
from streamlit_folium import st_folium





st.set_page_config(
    page_title="Eye Sight",
    page_icon=":bar_chart:",
    layout="wide"
)


@st.cache_data
def load_data():
    engine = create_engine(DB_URI)

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {TABLE_NAME}"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    return df


# Appel des données et refresh en appuyant sur un bouton
if st.button("Rafraichir mes données"):
    message = update_database()
    st.success(message, icon="🔥")
    load_data.clear()      # Vide le cache pour forcer un rechargement
    df = load_data()

else:
    df = load_data()



# Trier par date décroissante et garder les 5 plus récentes
df_recent = df.sort_values(by="start_date", ascending=False).head(5)


# ---- SIDEBAR ----
st.sidebar.header("Filtre ici 👇🏼 ")
sport = st.sidebar.multiselect(
    "Sélectionne ton sport:",
    options=df["sport_type"].unique()
)
weeks = st.sidebar.slider("Nombre de semaines à afficher sur les graphiques", 4, 52, 10)

df_selection = df.query(
    "sport_type == @sport"
)





# --- MAIN PAGE ---
st.title("Journal d'entrainement")
col1, col2 = st.columns(2)
with col1:
    run_week_progress(df, objectif_km=50)

st.markdown("""---""")

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Dernière activité")
    dernier = df.sort_values(by="start_date", ascending=False).iloc[0]
    st.write(f"**Type de sport :** {dernier['sport_type']}")
    st.write(f"**Distance :** {dernier['distance']:.2f} km")
    st.write(f"**Temps en mouvement :** {dernier['moving_time_hms']} s")
    st.write(f"**Vitesse moyenne :** {dernier['average_speed']:.2f} km/h")
    st.write(f"**Dénivelé positif :** {dernier['total_elevation_gain']:.0f} m")

    # Générer la carte
    m = create_latest_activity_map(df)

    if m is not None:
     # Afficher la carte dans Streamlit
        st_folium(m, width=700, height=500)
    else:
        st.warning("Pas de trace disponible pour la dernière activité.")

with middle_column:
    st.subheader("Kms en 2025 ")
    # Colonne date est bien en datetime
    df["date"] = pd.to_datetime(df["start_date"])
    # Filtrer l'année 2025
    df_2025 = df[(df["start_date"].dt.year == 2025)]

    # Filtrer uniquement les sports run et trail
    sports_voulus = ["Run", "TrailRun"]
    df_2025_run_trail = df_2025[df_2025["sport_type"].isin(sports_voulus)]

    # Somme des kilomètres
    km_2025 = df_2025_run_trail["distance"].sum()
    st.write(f"{km_2025:.2f} kilomètres")

with right_column:
    st.subheader("D+ à vie en trail")
    sports_voulus = ["TrainRun", "Run"]
    df_filtered = df[df["sport_type"].isin(sports_voulus)]
    d_plus = df_filtered["total_elevation_gain"].sum()
    st.write(f"{d_plus:.2f} d+ miam miam")

st.markdown("""---""")

st.dataframe(df_recent)


##. Heatmap calendar 2025

st.subheader("Heatmap de 2025")

fig = plot_calendar(df, year_min=2025, max_dist=20)

st.pyplot(fig)



## Plots

st.pyplot(plot_hours_per_week(df, weeks))

st.pyplot(plot_run_trail_km_per_week(df, weeks))

st.pyplot(plot_bike_km_per_week(df, weeks))

#st.pyplot(plot_swim_km_per_week(df, weeks))


# Slider pour choisir le nombre d'activités
num_activities = st.slider("Nombre d'activités les plus récentes à afficher", min_value=5, max_value=50, value=20)

df_recent = df.sort_values("start_date", ascending=False).head(num_activities)
df_recent = df_recent.sort_values("start_date")  # trier chronologiquement pour la courbe
st.pyplot(plot_heartrate(df_recent))



# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")

st.dataframe(df_selection)
