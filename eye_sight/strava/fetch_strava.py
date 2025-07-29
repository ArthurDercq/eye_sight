import requests
import pandas as pd
from datetime import datetime
from eye_sight.params import *



# Fonction pour récupérer les données depuis l'API Strava
def fetch_strava_data():

    # Obtenir la date actuelle
    #creation_date = datetime.now().strftime('%Y-%m-%d')

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

    # Liste pour stocker toutes les activités
    all_activities = []

    # Boucle pour récupérer toutes les pages d'activités
    page = 1
    while True:
        param = {'per_page': 200, 'page': page}
        activities = requests.get(ACTIVITES_URL, headers=header, params=param).json()

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

    return activities_df




def update_strava_data():

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
    print(f"✅ {len(df)} last activities retrieved from Strava.")
    return df
