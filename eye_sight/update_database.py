from eye_sight.strava.fetch_strava import update_strava_data
from eye_sight.strava.clean_data import clean_data
from eye_sight.strava.store_data import store_df_in_postgresql
from eye_sight.params import *
from sqlalchemy import create_engine, inspect, text
import requests
import pandas as pd



def update_strava_data():

    # Obtenir la date actuelle
    # creation_date = datetime.now().strftime('%Y-%m-%d')

    payload = {
    'client_id': STRAVA_CLIENT_ID,
    'client_secret': STRAVA_CLIENT_SECRET,
    'refresh_token': STRAVA_REFRESH_TOKEN,
    'grant_type': "refresh_token",
    'f': 'json'
    }

    print("Requesting Token...\n")
    res = requests.post(AUTH_URL, data=payload, verify=False)
    access_token = res.json()['access_token']
    print("Access Token = {}\n".format(access_token))

    header = {'Authorization': 'Bearer ' + access_token}
    params = {'per_page': 10, 'page': 1}

    print("📥 Fetching last 10 activities from Strava...")
    response = requests.get(ACTIVITES_URL, headers=header, params=params, timeout=30)
    response.raise_for_status()
    activities = response.json()

    if not activities:
        print("⚠️ No activities found.")
        return pd.DataFrame()

    df = pd.DataFrame(activities)
    print(f"✅ {len(df)} activities retrieved from Strava.")
    return df

def update_database():
    raw_df = update_strava_data()

    clean_df = clean_data(raw_df)

    store_df_in_postgresql(clean_df, host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)


if __name__ == "__main__":

    raw_df = update_strava_data()

    clean_df = clean_data(raw_df)

    store_df_in_postgresql(clean_df, host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)
