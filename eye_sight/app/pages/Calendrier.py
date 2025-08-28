import streamlit as st

st.set_page_config(layout="wide")

# --- CSS global ---
st.markdown("""
    <style>
    /* Fond dégradé */
    .stApp {
        background: linear-gradient(180deg, #6A75D1 0%, #9CA5E3 100%);
        color: #E5E7EB;
        font-family: 'Inter', sans-serif;
    }

    /* Titre principal */
    .main-title {
        font-size: 2.8rem;
        font-weight: 600;
        margin-bottom: 20px;
        color: #E5E7EB;
    }

    /* Bouton personnalisé */
    .refresh-btn {
        float: right;
        padding: 10px 20px;
        border-radius: 10px;
        background-color: rgba(31, 41, 52, 0.4);
        border: 1px solid #1F2934;
        color: #E5E7EB;
        font-weight: 500;
        cursor: pointer;
    }

    .refresh-btn:hover {
        background-color: rgba(31, 41, 52, 0.7);
    }

    /* Cards */
    .card {
        background-color: #1F2934;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }

    /* Section accomplissements */
    .accomplishments {
        display: flex;
        justify-content: space-around;
        align-items: center;
        background-color: #1F2934;
        padding: 20px;
        border-radius: 12px;
        margin-top: 30px;
        font-size: 1.2rem;
    }
    .accomplishments div {
        text-align: center;
    }
    .accomplishments .number {
        font-size: 2rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- Layout ---
st.markdown("<div class='main-title'>Mon journal d’entraînement</div>", unsafe_allow_html=True)
st.markdown("<button class='refresh-btn'>Rafraîchir mes données</button>", unsafe_allow_html=True)

col1, col2 = st.columns([2,1])
with col1:
    st.markdown("<div class='card'>Dernière activité</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='card'>Objectifs</div>", unsafe_allow_html=True)

col3, col4 = st.columns([2,1])
with col3:
    st.markdown("<div class='card'>Intensité</div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div class='card'>Suivi</div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>Heartrate distribution</div>", unsafe_allow_html=True)

st.markdown("""
<div class='accomplishments'>
    <div><span class="number">2500</span><br/>Kilomètres courus</div>
    <div><span class="number">7000</span><br/>Kilomètres roulés</div>
    <div><span class="number">3000</span><br/>Mètres grimpés</div>
</div>
""", unsafe_allow_html=True)
