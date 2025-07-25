from eye_sight.main import *
import streamlit as st
from sqlalchemy import create_engine
from eye_sight.params import DB_URI


#Get data

@st.cache_data
def load_data():
    engine = create_engine(DB_URI)
    query = "SELECT * FROM activities"
    df = pd.read_sql(query, engine)
    return df

# Appel dans Streamlit
st.title("Mes activités Strava")
df = load_data()
st.dataframe(df)

#KPIs to display
