from eye_sight.app.app import *


# =========================
# THEME CONFIG
# =========================
THEME = {
    "font": "Poppins, sans-serif",
    "title_color": "#1E3A8A",   # bleu foncé
    "subtitle_color" : "#3F589B",
    "kpi_bg": "#E0F2FE",        # bleu clair
    "progress": "#000000",
    "box_radius": "20px",
    "shadow": "0 4px 8px rgba(0, 0, 0, 0.1)"
}

# Inject custom CSS
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
        padding-top: 1.5rem;  /* met un petit padding minime */
    }}
    .title {{
        color: {THEME["title_color"]};
        font-weight: bold;
        font-size: 1.4rem;
        margin: 0.5rem 0;
    }}
    """, unsafe_allow_html=True
)

# --- Dataframe ---

# Colonnes à afficher
cols = [
    "start_date","name", "sport_type", "distance", "moving_time_hms",
    "speed_minutes_per_km_hms", "total_elevation_gain",
     "average_heartrate", "average_watts", "average_speed"
]

# Copie filtrée
df_formatted = df[cols].sort_values(by="start_date", ascending=False).copy()

## Gérer les Nan et les arrondis
df_formatted["distance"] = df_formatted["distance"].apply(
    lambda x: f"{x:.2f} km" if pd.notnull(x) else ""
)
df_formatted["average_heartrate"] = df_formatted["average_heartrate"].apply(
    lambda x: f"{int(round(x))} bpm" if pd.notnull(x) else ""
)
df_formatted["start_date"] = pd.to_datetime(df_formatted["start_date"]).dt.strftime("%d/%m/%Y")

# Colonne Vitesse/Allure
def format_speed(row):
    if row["sport_type"] == "Bike":
        return f"{row['average_speed']:.1f} km/h" if pd.notnull(row["average_speed"]) else ""
    else:
        return f"{row['speed_minutes_per_km_hms']} min/km" if pd.notnull(row["speed_minutes_per_km_hms"]) else ""

df_formatted["Vitesse/Allure"] = df_formatted.apply(format_speed, axis=1)
df_formatted = df_formatted.drop(columns=["speed_minutes_per_km_hms", "average_speed"])


# Ajouter les unités
df_formatted["total_elevation_gain"] = df_formatted["total_elevation_gain"].astype(str) + " m"
df_formatted["average_watts"] = df_formatted["average_watts"].astype(str) + " W"

#Renommer les colonnes proprement
df_formatted = df_formatted.rename(columns={
    "sport_type": "Sport",
    "distance": "Distance",
    "start_date": "Date",
    "name": "Activité",
    "moving_time_hms": "Durée",
    "total_elevation_gain": "D+",
    "average_heartrate": "FC moy",
    "average_watts": "Watts"
})


# Affichage

st.markdown('<div class="section-space">', unsafe_allow_html=True)
st.markdown("<div class='title'>Mes activités</div>", unsafe_allow_html=True)
st.markdown('<div class="section-space">', unsafe_allow_html=True)

if df.empty:
    st.warning("Aucunes données")
else:
    st.dataframe(
        df_formatted,
        use_container_width=True,
        hide_index=True
    )

st.markdown('<div class="section-space">', unsafe_allow_html=True)

df_sorted = df.sort_values(by="start_date", ascending=False)

activity_id = st.selectbox("Choisir l'activité à afficher", options=df_sorted["id"].tolist(),  # options = les ids réels
    format_func=lambda x: df_sorted.loc[df_sorted["id"] == x, "name"].values[0],  # afficher le nom
    index=0)

selected_activity = df_sorted[df_sorted["id"] == activity_id]

fig = create_latest_activity_poster(selected_activity)

if fig is None:
    st.warning("Aucune activité trouvée.")
else:
    #st.pyplot(fig)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=300, bbox_inches="tight", facecolor="black")
    buf.seek(0)

    st.download_button(
        label="📥 Télécharger l'affiche",
        data=buf,
        file_name="affiche_trail.png",
        mime="image/png"
    )
    st.image(buf)
