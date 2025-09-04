from eye_sight.strava.store_data import *
from eye_sight.strava.store_csv import *
from eye_sight.strava.clean_data import *
from eye_sight.strava.fetch_strava import *
from eye_sight.params import *


def create_database():

    raw_df = fetch_strava_data()

    clean_df = clean_data(raw_df)

    store_df_in_postgresql(clean_df, host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)

def create_database_streams():

    # 1. Récupère tous les IDs insérés
    activity_ids = get_all_activity_ids_from_db(DB_URI, TABLE_NAME)
    # 2. Récupère le header d'authentification Strava
    header = get_strava_header()
    # 3. Récupère les streams pour toutes les activités
    streams_df = fetch_multiple_streams_df(activity_ids, header)
    # 4. Stocke les streams dans PostgreSQL
    store_df_streams_in_postgresql(streams_df, host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)


if __name__ == '__main__':

    #create_database()
    create_database_streams()
