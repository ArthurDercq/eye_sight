import pandas as pd
import json


def convert_minutes_to_hms(minutes):

    if minutes is None or not isinstance(minutes, (int, float)):
        return "00:00:00"
    if minutes < 0:
        minutes = abs(minutes)

    total_seconds = int(minutes * 60)
    h = total_seconds // 3600
    remainder = total_seconds % 3600
    m = remainder // 60
    s = remainder % 60
    return f"{h:02}:{m:02}:{s:02}"


def format_pace(speed_kmh):

    if pd.isna(speed_kmh) or speed_kmh == 0:
        return None
    total_minutes = 60 / speed_kmh
    minutes = int(total_minutes)
    seconds = int(round((total_minutes - minutes) * 60))
    return f"{minutes}:{seconds:02d}"  # format mm:ss


# Fonction pour nettoyer les données
def clean_data(df):

    # Copier le DataFrame pour ne pas modifier l'original
    activities_df_cleaned = df.copy()

    # Liste des colonnes à supprimer
    columns_to_drop = [
    'resource_state', 'athlete', 'type', 'workout_type', 'utc_offset',
    'location_city', 'location_state', 'location_country', 'comment_count',
    'athlete_count', 'photo_count', 'trainer', 'commute', 'manual',
    'private', 'visibility', 'flagged', 'device_watts', 'heartrate_opt_out',
    'display_hide_heartrate_option', 'upload_id', 'upload_id_str', 'external_id',
    'from_accepted_tag', 'total_photo_count'
    ]
    # Suppression des colonnes non pertinentes du DataFrame
    activities_df_cleaned.drop(columns=columns_to_drop, errors='ignore', inplace=True)
    print("Colonnes ✅")

    # Conversion de la colonne 'distance' de mètres en kilomètres
    activities_df_cleaned['distance'] = activities_df_cleaned['distance'] / 1000
    print("Distance convertie ✅")


    # Conversion des colonnes 'moving_time' et 'elapsed_time' de secondes en minutes
    activities_df_cleaned['moving_time'] = activities_df_cleaned['moving_time'] / 60
    activities_df_cleaned['elapsed_time'] = activities_df_cleaned['elapsed_time'] / 60
    print("temps de secondes en minutes ✅")


    # Conversion de la colonne 'average_speed' de mètres par seconde en kilomètres par heure
    activities_df_cleaned['average_speed'] = activities_df_cleaned['average_speed'] * 3.6
    activities_df_cleaned['max_speed'] = activities_df_cleaned['max_speed'] * 3.6
    print("m/s en km/h ✅")


    # Ajouter une nouvelle colonne 'minutes_per_km' qui convertit 'average_speed' en minutes par kilomètre
    activities_df_cleaned['speed_minutes_per_km'] = activities_df_cleaned['average_speed'].apply(format_pace)
    print("min/km colonne ✅")


    # Ajouter une nouvelle colonne avec le format HH:MM:SS pour 'moving_time' et 'elapsed_time'
    activities_df_cleaned['moving_time_hms'] = activities_df_cleaned['moving_time'].apply(convert_minutes_to_hms)
    activities_df_cleaned['elapsed_time_hms'] = activities_df_cleaned['elapsed_time'].apply(convert_minutes_to_hms)
    print("Format temps HH:MM:SS ✅")

    # Sérialisation du champ map
    activities_df_cleaned["map"] = activities_df_cleaned["map"].apply(json.dumps)

    required_columns = [
    'id', 'name', 'distance', 'moving_time', 'moving_time_hms',
    'elapsed_time_hms', 'start_date', 'type', 'sport_type', 'workout_type',
    'total_elevation_gain', 'start_latitude', 'start_longitude', 'end_latitude',
    'end_longitude', 'location_city', 'location_state', 'location_country',
    'achievement_count', 'kudos_count', 'comment_count', 'athlete_count',
    'photo_count', 'trainer', 'commute', 'manual', 'private', 'visibility',
    'max_speed', 'average_cadence', 'average_temp', 'has_heartrate',
    'average_heartrate', 'max_heartrate', 'elev_high', 'elev_low', 'pr_count',
    'has_kudoed', 'average_watts', 'kilojoules', 'map'
]

# Ajouter les colonnes manquantes avec None
    for col in required_columns:
        if col not in activities_df_cleaned.columns:
            activities_df_cleaned[col] = None

    print("Les données ont été nettoyées avec succès ✅")


    return activities_df_cleaned
