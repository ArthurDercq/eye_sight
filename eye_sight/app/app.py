from eye_sight.main import *
from eye_sight.update_database import update_database
import streamlit as st
from sqlalchemy import create_engine, text
from eye_sight.params import *
import altair as alt
from eye_sight.plots.plot_calendar_heat import plot_calendar




@st.cache_data
def load_data():
    engine = create_engine(DB_URI)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM dashboard"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    return df


# Refresh des données en appuyant sur bouton
# Bouton
if st.button("Rafraichir mes données"):
    update_database()

#Appel des données
df = load_data()


# Trier par date décroissante et garder les 5 plus récentes
df_recent = df.sort_values(by="start_date", ascending=False).head(5)


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
sport = st.sidebar.multiselect(
    "Select the sport:",
    options=df["sport_type"].unique()
)

df_selection = df.query(
    "sport_type == @sport"
)



# --- MAIN PAGE ---
st.title("Journal d'entrainement")
st.markdown("##")

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Dernière activité")
    dernier = df.sort_values(by="start_date", ascending=False).iloc[1]
    st.write(f"**Type de sport :** {dernier['sport_type']}")
    st.write(f"**Distance :** {dernier['distance']:.2f} km")
    st.write(f"**Temps en mouvement :** {dernier['moving_time_hms']} s")
    st.write(f"**Vitesse moyenne :** {dernier['average_speed']:.2f} km/h")
    st.write(f"**Dénivelé positif :** {dernier['total_elevation_gain']:.0f} m")

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

fig = plot_calendar(df, year_min=2025, max_dist=20)

st.pyplot(fig)


# Check if the dataframe is empty:
if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop() # This will halt the app from further execution.

st.dataframe(df_selection)
