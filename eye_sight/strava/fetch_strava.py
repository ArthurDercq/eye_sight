import requests
import pandas as pd
from datetime import datetime
from eye_sight.params import *



# Fonction pour récupérer les données depuis l'API Strava
def fetch_strava_data():
    auth_url = "https://www.strava.com/oauth/token"
    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    # Obtenir la date actuelle
    creation_date = datetime.now().strftime('%Y-%m-%d')

    payload = {
    'client_id': STRAVA_CLIENT_ID,
    'client_secret': STRAVA_CLIENT_SECRET,
    'refresh_token': STRAVA_REFRESH_TOKEN,
    'grant_type': "refresh_token",
    'f': 'json'
    }

    print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']
    print("Access Token = {}\n".format(access_token))

    header = {'Authorization': 'Bearer ' + access_token}

    # Liste pour stocker toutes les activités
    all_activities = []

    # Boucle pour récupérer toutes les pages d'activités
    page = 1
    while True:
        param = {'per_page': 200, 'page': page}
        activities = requests.get(activites_url, headers=header, params=param).json()

        # Si aucune activité n'est retournée, on arrête la boucle
        if not activities:
            break

    # Ajout des activités à la liste
    all_activities.extend(activities)

    # Incrémentation du numéro de page
    page += 1

    # Conversion en DataFrame pandas
    activities_df = pd.DataFrame(all_activities)

    # Sauvegarde en fichier CSV
    #csv_file_path = f'../data/strava_activities_raw_{creation_date}.csv'
    #activities_df.to_csv(csv_file_path, index=False)

    print("Données récupérées de l'API Strava ✅")

    #print(f"Les données ont aussi été sauvegardées en .csv dans {csv_file_path} ✅")

    return activities_df
