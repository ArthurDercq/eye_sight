from eye_sight.strava.store_data import *
from eye_sight.strava.store_csv import *
from eye_sight.strava.clean_data import *
from eye_sight.strava.fetch_strava import *
from eye_sight.params import *


def create_database():

    raw_df = fetch_strava_data()

    clean_df = clean_data(raw_df)

    store_df_in_postgresql(clean_df, host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)


if __name__ == '__main__':

    create_database()
