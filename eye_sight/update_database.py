from eye_sight.strava.fetch_strava import *
from eye_sight.strava.clean_data import clean_data
from eye_sight.strava.store_data import store_df_in_postgresql
from eye_sight.params import *
from sqlalchemy import create_engine, text



def get_last_activity_date():

    engine = create_engine(DB_URI)
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT MAX(start_date) FROM {TABLE_NAME}")) #choppe la dernière date d'acti
        last_date = result.scalar()
    return last_date


def update_strava():
    last_date = get_last_activity_date()

    # Récupère les données de Strava (ou autre) après cette date
    new_data = fetch_strava_data(after_date=last_date)

    if new_data.empty:
        return None

    cleaned_data = clean_data(new_data)

    return cleaned_data


def update_database():

    cleaned_data = update_strava()

    if cleaned_data is None:
        return "Aucune nouvelle activité trouvée."

    store_df_in_postgresql(cleaned_data, host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)

    return f"{len(cleaned_data)} nouvelle(s) activité(s) ajoutée(s)."





if __name__ == "__main__":

    raw_df = update_strava()

    cleaned_data = clean_data(raw_df)

    store_df_in_postgresql(cleaned_data, host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)
