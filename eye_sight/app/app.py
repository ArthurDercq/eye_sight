import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from streamlit_folium import st_folium


# Imports locaux
from eye_sight.update_database import update_database
from eye_sight.params import DB_URI, TABLE_NAME
from eye_sight.plots.plot_calendar_heat import plot_calendar
from eye_sight.plots.basic_plots import *
from eye_sight.plots.plot_map import *


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
    "title_color": "#1E3A8A",   # bleu foncé
    "subtitle_color" : "#3F589B",
    "box_title_color" : "#E5E7EB",
    "kpi_bg": "#E0F2FE",        # bleu clair
    "progress": "#000000",
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
        color: #E5E7EB;
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
        background-color: rgba(31, 41, 52, 0.7);
        color: #ffffff;
    }}
    .stProgress > div > div > div > div {{
        background-color: #6466EA !important;
    }}
    .bento-box {{
        background-color: #1F2934;
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
        color: {THEME["title_color"]};
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


# --- Définition semaine ---
if "week_offset" not in st.session_state:
    st.session_state.week_offset = 0

today = pd.Timestamp.today().normalize()
week_start = today - pd.to_timedelta(today.weekday(), unit="D") + pd.Timedelta(weeks=st.session_state.week_offset)
week_end = week_start + pd.Timedelta(days=6)


# --- 2 box intro ---

st.markdown('<div class="section-space">', unsafe_allow_html=True)

col1, col2 = st.columns([2,1.5])
with col1:
    dernier = df.sort_values(by="start_date", ascending=False).iloc[0]
    st.markdown(f"""
        <div class='bento-box'>
            <div class='box-title'>Dernière activité
            <div class='box-element'> Type:</b> {dernier['sport_type']}</p>
            <p><b>Distance:</b> {dernier['distance']:.2f} km</p>
            <p><b>Durée:</b> {dernier['moving_time_hms']}</p>
            <p><b>Allure moy.:</b> {dernier['speed_minutes_per_km_hms']} min/km ({dernier['average_speed']:.2f} km/h)</p>
            <p><b>D+:</b> {dernier['total_elevation_gain']:.0f} m</p>
            <p><b>BPM moyen:</b> {dernier['average_heartrate']}</p>
        </div>
        """, unsafe_allow_html=True)

with col2:

    progression, km_total, start_week, end_week, objectif_km = run_week_progress(df, objectif_km=50)

    # Ouvre la box
    st.markdown(f"""
    <div class='bento-box'>
        <span style='font-size:1.5rem; font-weight:600;'>Objectifs</span>
        <span style='font-size:0.6rem; font-weight:200; color:#D1D5DB; margin-left:8px;'>
            Semaine du {week_start.strftime('%d/%m')} au {week_end.strftime('%d/%m')}
        </span>
        <div style='margin-top:10px;'>
    """, unsafe_allow_html=True)

    # Composants Streamlit "dans" la box
    st.progress(progression)
    st.markdown(f"<div class='subtitle progress'>{km_total:.1f} kms parcourus / {objectif_km} kms</div>", unsafe_allow_html=True)

    # Ferme la box
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)







st.markdown("<div class='title'>Minutes d'intensité</div>", unsafe_allow_html=True)
st.pyplot(plot_weekly_intensity(df,week_start, week_end))
st.markdown('</div>', unsafe_allow_html=True)




# --- KPIs ---
st.markdown('<div class="section-space">', unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)
with col1:
    km_run_2025 = df[df["start_date"].dt.year == 2025].query("sport_type in ['Run','Trail']")["distance"].sum()
    st.markdown(f"<div class='bento-box kpi-box'>🏃 {km_run_2025:.1f} km en 2025</div>".replace(",", " "), unsafe_allow_html=True)

with col2:
    km_bike_2025 = df[df["start_date"].dt.year == 2025].query("sport_type in ['Bike']")["distance"].sum()
    st.markdown(f"<div class='bento-box kpi-box'>🚴🏼 {km_bike_2025:.1f} km en 2025</div>", unsafe_allow_html=True)
with col3:
    d_plus = df[df["start_date"].dt.year == 2025].query("sport_type in ['Trail','Run', 'Bike']")["total_elevation_gain"].sum()
    st.markdown(f"<div class='bento-box kpi-box'>⛰️ {d_plus:.0f} m D+ en 2025</div>", unsafe_allow_html=True)


st.markdown('</div>', unsafe_allow_html=True)


# --- Dernière activité ---
st.markdown('<div class="section-space">', unsafe_allow_html=True)
st.markdown("<div class='subtitle progress'>Choisis le sport à afficher</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Initialisation si pas encore définie
if "selected_sport" not in st.session_state:
    st.session_state.selected_sport = "Run"  # valeur par défaut
# 4 boutons côte à côte
col1, col2, col3, col4, _ = st.columns([1,1,1,1,5])  # les 4 premiers = boutons, le dernier = espace vide


with col1:
    if st.button("Trail", key="btn_trail"):
        st.session_state.selected_sport = "Trail"
with col2:
    if st.button("Course", key="btn_course"):
        st.session_state.selected_sport = "Run"
with col3:
    if st.button("Vélo", key="btn_velo"):
        st.session_state.selected_sport = "Bike"
with col4:
    if st.button("Natation", key="btn_swim"):
        st.session_state.selected_sport = "Swim"


# Récupérer la dernière activité du sport choisi
df_filtered = df[df["sport_type"] == st.session_state.selected_sport]
if not df_filtered.empty:
    dernier = df_filtered.sort_values(by="start_date", ascending=False).iloc[0]

    colA, colB = st.columns([1,2])
    with colA:
        st.markdown(f"""
        <div class='bento-box'>
            <div class='box_title'>Dernière activité
            <div class='box_element'> Type:</b> {dernier['sport_type']}</p>
            <p><b>Distance:</b> {dernier['distance']:.2f} km</p>
            <p><b>Durée:</b> {dernier['moving_time_hms']}</p>
            <p><b>Allure moy.:</b> {dernier['speed_minutes_per_km_hms']} min/km ({dernier['average_speed']:.2f} km/h)</p>
            <p><b>D+:</b> {dernier['total_elevation_gain']:.0f} m</p>
            <p><b>BPM moyen:</b> {dernier['average_heartrate']}</p>
        </div>
        """, unsafe_allow_html=True)

    with colB:
        m = create_latest_activity_map(df_filtered)
        if m is not None:
            st_folium(m, width=700, height=500)
        else:
            st.warning("Pas de trace disponible pour ce sport.")


        st.pyplot(plot_mini_map(df_filtered))
else:
    st.warning("Aucune activité trouvée pour ce sport 🚫")



# --- Graphiques 2 par 2 ---
st.markdown("<div class='title'>Graphiques</div>", unsafe_allow_html=True)

weeks = 10 ## Nombre de semaines à afficher par défaut

charts = [
    ("📅 Heatmap 2025", plot_calendar(df, year_min=2025, max_dist=20)),
    ("🕒 Heures par semaine", plot_hours_per_week(df, weeks)),
    ("🏃 Km Run/Trail par semaine", plot_run_trail_km_per_week(df, weeks)),
    ("🚴 Km Vélo par semaine", plot_bike_km_per_week(df, weeks))
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
