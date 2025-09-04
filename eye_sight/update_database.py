from eye_sight.strava.fetch_strava import *
from eye_sight.strava.clean_data import clean_data
from eye_sight.strava.store_data import store_df_in_postgresql
from eye_sight.params import *
from sqlalchemy import create_engine, text
from eye_sight.strava.fetch_strava import fetch_multiple_streams_df, get_strava_header
from eye_sight.strava.store_data import store_df_streams_in_postgresql


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

    return new_data


def update_database():

    new_data = update_strava()

    if new_data is None:
        return "Aucune nouvelle activité trouvée"

    cleaned_data = clean_data(new_data)

    store_df_in_postgresql(cleaned_data, host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)

    return f"{len(cleaned_data)} nouvelle(s) activité(s) ajoutée(s)"




def update_streams_database():
    # Récupère les nouvelles activités
    new_data = update_strava()
    if new_data is None:
        return "Aucune nouvelle activité trouvée"

    # Récupère les IDs des nouvelles activités
    activity_ids = new_data["id"].tolist()
    if not activity_ids:
        return "Aucun nouvel ID d'activité"

    # Récupère le header d'authentification
    header = get_strava_header()

    # Récupère les streams pour ces activités
    streams_df = fetch_multiple_streams_df(activity_ids, header)

    if streams_df.empty:
        return "Aucun stream récupéré"

    # Stocke les streams dans PostgreSQL
    store_df_streams_in_postgresql(streams_df, host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)

    return f"{len(streams_df)} stream(s) ajouté(s)"



if __name__ == "__main__":

    update_database()
    update_streams_database()
