from eye_sight.strava.clean_data import *
from sqlalchemy import create_engine, text
from eye_sight.params import *
from eye_sight.strava.fetch_strava import *
import pandas as pd
from datetime import datetime


def store_df_in_csv(df, db_path):

    # Exporter le DataFrame nettoyé en fichier CSV
    df.to_csv(db_path, index=False)

    print("Database sauvegardée en csv ✅")


def load_data():
    engine = create_engine(DB_URI)

    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {TABLE_NAME}"))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())

    return df

if __name__ == '__main__':

    date = datetime.now().date()

    df = load_data()
    #df = fetch_strava_data()
    clean_df = clean_data(df)

    store_df_in_csv(clean_df, f"/Users/arthurdercq/code/Data Science/Garmin_Dashboard/data/clean_data_{date}.csv")
