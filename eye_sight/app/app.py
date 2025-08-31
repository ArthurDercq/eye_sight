import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from streamlit_folium import st_folium
import math
import io


# Imports locaux
from eye_sight.update_database import update_database
from eye_sight.params import DB_URI, TABLE_NAME
from eye_sight.plots.plot_calendar_heat import plot_calendar
from eye_sight.plots.basic_plots import *
from eye_sight.plots.plot_map import *
from eye_sight.plots.art import *


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Eye Sight",
    page_icon=":bar_chart:",
    layout="wide"
)

# =========================
# THEME CONFIG
# =========================
THEME = {
    "font": "Poppins, sans-serif",
    "title-color": "#1E3A8A",   # bleu foncé
    "subtitle_color" : "#3F589B",
    "box_title_color" : "#E5E7EB",
    "box-element-label-color":"#D1D5DB",
    "kpi_bg": "#E0F2FE",        # bleu clair
    "progress": "#000000",
    "background-color":"#1F2934",
    "box_radius": "10px",
    "shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
}

# Custom CSS
st.markdown(f"""
    <style>
    * {{
        font-family: {THEME["font"]};
    }}
    /* Réduire l’espace en haut de page */
    .css-18e3th9 {{
        padding-top: 0rem;
        padding-bottom: 0rem;
    }}

    /* Si besoin, ajuster aussi le padding du contenu principal */
    .block-container {{
        padding-top: 3.5rem;  /* met un petit padding minime */
    }}

    /* Titre principal */
    .main-title {{
        font-size: 2.8rem;
        font-weight: 600;
        margin-bottom: 20px;
        color: {THEME["background-color"]};
    }}
    /* Bouton personnalisé */
    div.stButton > button:first-child {{
        background-color: rgba(31, 41, 52, 0.4);
        color: #E5E7EB;
        border: 1px solid #1F2934;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 500;
        cursor: pointer;
    }}
    div.stButton > button:first-child:hover {{
        background-color: {THEME["background-color"]};
        color: #ffffff;
    }}
    .stProgress > div > div > div > div {{
        background-color: #6466EA !important;
    }}
    .bento-box {{
        background-color: {THEME["background-color"]};
        border-radius: {THEME["box_radius"]};
        box-shadow: {THEME["shadow"]};
        padding: 1rem;
        margin-bottom: 1rem;
    }}
    .kpi-box {{
        background-color: {THEME["kpi_bg"]};
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }}
    .title {{
        color: {THEME["title-color"]};
        font-weight: bold;
        font-size: 1.4rem;
        margin: 0.5rem 0;
    }}
    .box-title {{
        color: {THEME["box_title_color"]};
        font-weight: bold;
        font-size: 1.4rem;
        margin: 0.5rem 0;
    }}
    .box-element {{
        color: {THEME["box_title_color"]};
        font-weight: normal;
        font-size: 1rem;
        margin: 0.5rem 0;
    }}
    .box-label {{
        font-size:0.6rem;
        font-weight:200;
        color:{THEME["box-element-label-color"]};
        margin-right:8px;
    }}
    .subtitle {{
        color: {THEME["subtitle_color"]};
        font-weight: 400;
        font-size: 1rem;
        margin: 0.25rem 0 0.75rem 0;
    }}
    .progress {{
        color: {THEME["progress"]};
    }}
    .section-space {{ margin-top: 2rem; margin-bottom: 2rem; }}

    /* Section accomplissements */
    .accomplishments {{
        color: {THEME["box_title_color"]};
        display: flex;
        justify-content: space-around;
        align-items: center;
        background-color: #1F2934;
        padding: 20px;
        border-radius: 12px;
        margin-top: 30px;
        font-size: 1.2rem;
    }}
    .accomplishments div {{
        text-align: center;
    }}
    .accomplishments .number {{
        font-size: 2rem;
        font-weight: 600;
    }}
    </style>
""", unsafe_allow_html=True)



# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    engine = create_engine(DB_URI)
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {TABLE_NAME}"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


# =========================
# HEADER & REFRESH DATA
# =========================

st.markdown("<div class='main-title'>Mon journal d’entraînement</div>", unsafe_allow_html=True)

# --- Refresh bouton ---
if st.button("Rafraîchir mes données"):
    message = update_database()
    st.success(message, icon="🔥")
    load_data.clear()
    df = load_data()
else:
    df = load_data()

# =========================
# SIDEBAR
# =========================
#st.sidebar.header("🎯 Filtres")
#sport = st.sidebar.multiselect(
#    "Sélectionne ton sport:",
#    options=df["sport_type"].unique()
#)
#weeks = st.sidebar.slider("Nombre de semaines à afficher", 4, 52, 10)

#df_selection = df.query("sport_type == @sport") if sport else df


# =========================
# MAIN PAGE
# =========================



# =========================
# INTRO
# =========================

st.markdown('<div class="section-space">', unsafe_allow_html=True)

c1,c2 = st.columns([2,20])
with c1:
# Liste des sports disponibles
    sports = ["Trail", "Run", "Bike", "Swim"]

    # Multiselect
    selected_sport = st.selectbox("",
        options=sports,
        index=1  # tu peux mettre une sélection par défaut
    )

col1, col2 = st.columns([2,1.5])
with col1:


    # Filtrer le DF en fonction du choix
    df_filtered = df[df["sport_type"] == selected_sport].sort_values(
    by="start_date", ascending=False
    )

    if not df_filtered.empty:
    # On prend la dernière activité correspondant au filtre
        dernier = df_filtered.iloc[0]

        st.markdown(f"""
        <div class='bento-box'>
            <div class='box-title'>Dernière activité</div>
            <span class='box-label'>Type</span>  <span class='box-element'>{dernier['sport_type']}</span></p>
            <p><span class='box-label'>Distance </b> </span><span class='box-element'>{dernier['distance']:.2f} km</span></p>
            <p><span class='box-label'>Durée </b> </span><span class='box-element'>{dernier['moving_time_hms']}</span></p>
            <p><span class='box-label'>Allure moyenne </b></span> <span class='box-element'>{dernier['speed_minutes_per_km_hms']} min/km ({dernier['average_speed']:.2f} km/h)</span></p>
            <p><span class='box-label'>D+ </b> </span><span class='box-element'>{dernier['total_elevation_gain']:.0f} m</span></p>
            <p><span class='box-label'>BPM moyen </b></span> <span class='box-element'>{dernier['average_heartrate']} bpm</span></p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("Aucune activité trouvée pour ce sport.")



with col2:
    dernier_map = df_filtered.iloc[[0]]
    st.pyplot(plot_mini_map(dernier_map))

    #m = create_latest_activity_map(dernier_map)
    #if m is not None:
    #    st_folium(m, width=700, height=500)
    #else:
    #    st.warning("Pas de trace disponible pour ce sport.")

st.markdown('</div>', unsafe_allow_html=True)


st.markdown('<div class="section-space">', unsafe_allow_html=True)


# =========================
# INTRO
# =========================

if "week_offset" not in st.session_state:
    st.session_state.week_offset = 0

today = pd.Timestamp.today().normalize()

# Générer une liste des dernières semaines (ex: 10 dernières)
weeks = []
for i in range(10):
    start = today - pd.to_timedelta(today.weekday(), unit="D") - pd.Timedelta(weeks=i)
    end = start + pd.Timedelta(days=6)
    weeks.append((start, end))
#week_start = today - pd.to_timedelta(today.weekday(), unit="D") + pd.Timedelta(weeks=st.session_state.week_offset)
#week_end = week_start + pd.Timedelta(days=6)
# Créer des labels lisibles pour l'utilisateur
week_labels = [f"Semaine du {s.strftime('%d/%m')} au {e.strftime('%d/%m')}" for s, e in weeks]

# Selectbox pour choisir la semaine
c1,c2 = st.columns([2,6])
with c1:
    selected_label = st.selectbox("", week_labels)

# Récupérer les bornes en fonction du choix
selected_index = week_labels.index(selected_label)
week_start, week_end = weeks[selected_index]
progression, km_total, start_week, end_week, objectif_km = run_week_progress(df, objectif_km=50)

# Ouvre la box
st.markdown(f"""
    <div class='bento-box'>
        <div class='box-title'>Objectifs </div>
        <span style='font-size:0.6rem; font-weight:200; color:#D1D5DB; margin-left:8px;'>
            Semaine du {week_start.strftime('%d/%m')} au {week_end.strftime('%d/%m')}
        </span>
        <div style='margin-top:10px;'>
    """, unsafe_allow_html=True)

    # Composants Streamlit "dans" la box
st.progress(progression)
st.markdown(f"<div class='subtitle progress'>{km_total:.1f} kms parcourus / {objectif_km} kms</div>", unsafe_allow_html=True)

    # Ferme la box
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# =========================
# KPI 2025
# =========================

st.markdown('<div class="section-space">', unsafe_allow_html=True)

km_run_2025 = df[df["start_date"].dt.year == 2025].query("sport_type in ['Run','Trail']")["distance"].sum()
km_run_2025_ceil = math.ceil(km_run_2025)
km_run_2025_fr = f"{km_run_2025_ceil:,}".replace(",", " ")


km_bike_2025 = df[df["start_date"].dt.year == 2025].query("sport_type in ['Bike']")["distance"].sum()
km_bike_2025_ceil = math.ceil(km_bike_2025)
km_bike_2025_fr = f"{km_bike_2025_ceil:,}".replace(",", " ")

d_plus = df[df["start_date"].dt.year == 2025].query("sport_type in ['Trail','Run', 'Bike']")["total_elevation_gain"].sum()
d_plus_ceil = math.ceil(d_plus)
d_plus_fr = f"{d_plus_ceil:,}".replace(",", " ")

st.markdown(f"""
<div class='accomplishments'>
    <div><span class="number">{km_run_2025_fr}</span><br/>Kilomètres courus</div>
    <div><span class="number">{km_bike_2025_fr}</span><br/>Kilomètres roulés</div>
    <div><span class="number">{d_plus_fr}</span><br/>Mètres grimpés</div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)






# =========================
# Graphiques
# =========================

st.markdown('<div class="section-space">', unsafe_allow_html=True)


#weeks = 10 ## Nombre de semaines à afficher par défaut

# Générer une liste des dernières semaines (ex: 10 dernières)
weeks = []
for i in range(10):
    start = today - pd.to_timedelta(today.weekday(), unit="D") - pd.Timedelta(weeks=i)
    end = start + pd.Timedelta(days=6)
    weeks.append((start, end))
week_labels = [f"Semaine du {s.strftime('%d/%m')} au {e.strftime('%d/%m')}" for s, e in weeks]

c1,c2 = st.columns([1,4])
with c1:
    selected_week = st.selectbox("Choisis la semaine :", week_labels)
    # Récupérer les bornes de la semaine sélectionnée
    selected_index = week_labels.index(selected_week)
    week_start, week_end = weeks[selected_index]

    df_week = df[
        (df["start_date"].dt.date >= week_start.date()) &
        (df["start_date"].dt.date <= week_end.date())
    ].copy()

    sport_label= ["Trail", "Run"]
    select_sport = st.selectbox("Choisis le sport :", sport_label, index=1)

charts = [
    ("📅 Heatmap 2025", plot_calendar(df, year_min=2025, max_dist=20)),
    ("🕒 Heures par semaine", plot_hours_per_week(df, weeks=10)),
    ("🏃 Km Run/Trail par semaine", plot_run_trail_km_per_week(df, weeks=10)),
    ("🚴 Km Vélo par semaine", plot_bike_km_per_week(df, weeks=10)),
    (" Intensité", plot_weekly_intensity(df,week_start, week_end)),
    (f"Répartition par type de sortie - {select_sport}", plot_repartition_run(df_week, sport_type=select_sport))
]

for i in range(0, len(charts), 2):
    col1, col2 = st.columns(2)
    with col1:
        title, fig = charts[i]
        st.markdown(f"<div class='title'>{title}</div>", unsafe_allow_html=True)
        st.pyplot(fig)
    if i+1 < len(charts):
        with col2:
            title, fig = charts[i+1]
            st.markdown(f"<div class='title'>{title}</div>", unsafe_allow_html=True)
            st.pyplot(fig)


# --- Activités récentes avec HR ---
st.markdown("<div class='title'>Fréquence cardiaque - dernières activités</div>", unsafe_allow_html=True)
num_activities = st.slider("Nombre d'activités", 5, 50, 20)
df_recent = df.sort_values("start_date", ascending=False).head(num_activities).sort_values("start_date")
st.pyplot(plot_heartrate(df_recent))


st.markdown('</div>', unsafe_allow_html=True)




st.markdown('<div class="section-space">', unsafe_allow_html=True)


st.markdown('</div>', unsafe_allow_html=True)
