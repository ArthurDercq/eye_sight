from eye_sight.main import *
import streamlit as st
from sqlalchemy import create_engine, text
from eye_sight.params import *


#Get data

#@st.cache_data
def load_data():
    engine = create_engine(DB_URI)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM dashboard"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    return df

# Appel dans Streamlit
st.title("Mon dashboard")
df = load_data()
st.dataframe(df)

#KPIs to display
