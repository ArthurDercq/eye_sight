from eye_sight.strava.store_data import *
from eye_sight.strava.clean_data import *
from eye_sight.strava.fetch_strava import *
from eye_sight.params import *


def main():

    raw_df = fetch_strava_data()

    clean_df = clean_data(raw_df)

    store_df_in_csv(clean_df, DB_PATH)

    store_df_in_postgresql(clean_df, host=host, database=database, user=user, password=password, port=port)


if __name__ == '__main__':

    main()
