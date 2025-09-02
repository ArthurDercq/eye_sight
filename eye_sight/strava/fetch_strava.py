import requests
import pandas as pd
from pandas import Timestamp
from datetime import datetime
from eye_sight.params import *



# Fonction pour récupérer les données depuis l'API Strava
def fetch_strava_data(after_date = None, return_header=False):

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


    # Si une date est fournie, la convertir en timestamp Unix pour Strava
    after_timestamp = None
    if after_date:
        after_timestamp = int(after_date.timestamp())
        print(f"⏩ Récupération des activités après {after_date} (timestamp={after_timestamp})")


    # Liste pour stocker toutes les activités
    all_activities = []

    # Boucle pour récupérer toutes les pages d'activités
    page = 1
    while True:
        params = {'per_page': 200, 'page': page}
        if after_timestamp:
            params['after'] = after_timestamp

        activities = requests.get(ACTIVITES_URL, headers=header, params=params).json()

        # Si aucune activité n'est retournée, on arrête la boucle
        if not activities:
            break

        # Ajout des activités à la liste
        all_activities.extend(activities)

        print(f"📄 Page {page}…")
        # Incrémentation du numéro de page
        page += 1

    # Conversion en DataFrame pandas
    activities_df = pd.DataFrame(all_activities)


    print("Données récupérées de l'API Strava ✅")

    # Retour conditionnel
    if return_header:
        return activities_df, header
    else:
        return activities_df


def fetch_streams(activity_id, header):

    #Récupère les streams (altitude, distance, latlng, time) d'une activité

    url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams"
    params = {"keys": "latlng,altitude,distance,time", "key_by_type": "true"}
    resp = requests.get(url, headers=header, params=params)
    resp.raise_for_status()
    streams = resp.json()

    latlng = streams.get("latlng", {}).get("data", [])
    altitude = streams.get("altitude", {}).get("data", [])
    distance = streams.get("distance", {}).get("data", [])
    time = streams.get("time", {}).get("data", [])

    # Construction DataFrame
    df_stream = pd.DataFrame({
        "activity_id": activity_id,
        "lat": [pt[0] for pt in latlng] if latlng else None,
        "lon": [pt[1] for pt in latlng] if latlng else None,
        "altitude": altitude,
        "distance_m": distance,
        "time_s": time
    })

    return df_stream
