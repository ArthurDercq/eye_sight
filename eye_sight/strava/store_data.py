
import pandas as pd
import sqlite3
from psycopg2 import connect, sql
from psycopg2.extras import execute_values
import pandas as pd
import json
from datetime import datetime
from eye_sight.strava.clean_data import *
from eye_sight.strava.fetch_strava import *
from eye_sight.params import *
from datetime import datetime






def store_df_in_sqlite(df, db_path, table_name=TABLE_NAME):
    #Stocke un DataFrame dans une base de données SQLite
    conn = sqlite3.connect(db_path)
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data successfully stored in {table_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


def normalize_sport_type(sport):
    mapping = {
        "Ride": "Bike",
        "TrainRun": "Trail"
    }
    return mapping.get(sport, sport)

def store_df_in_postgresql(df, host, database, user, password, port):

    # Connexion à la DB
    conn = connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )
    cur = conn.cursor()

    table_name = TABLE_NAME

    # Création de la table (si elle n'existe pas)
    create_table_query = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {} (
        id BIGSERIAL PRIMARY KEY,
        name VARCHAR(255),
        distance FLOAT,
        moving_time FLOAT,
        elapsed_time FLOAT,
        moving_time_hms TEXT,
        elapsed_time_hms TEXT,
        average_speed FLOAT,
        speed_minutes_per_km FLOAT,
        speed_minutes_per_km_hms TEXT,
        total_elevation_gain FLOAT,
        sport_type VARCHAR(255),
        start_date TIMESTAMP,
        start_date_local TIMESTAMP,
        timezone VARCHAR(50),
        achievement_count INTEGER,
        kudos_count INTEGER,
        gear_id VARCHAR(255),
        start_latlng VARCHAR(50),
        end_latlng VARCHAR(50),
        max_speed FLOAT,
        average_cadence FLOAT,
        average_temp FLOAT,
        has_heartrate BOOLEAN,
        average_heartrate FLOAT,
        max_heartrate FLOAT,
        elev_high FLOAT,
        elev_low FLOAT,
        pr_count INTEGER,
        has_kudoed BOOLEAN,
        average_watts FLOAT,
        kilojoules FLOAT,
        map JSONB
    );
    """).format(sql.Identifier(table_name))

    cur.execute(create_table_query)

    # Préparer les données
    values = [
        (
        row['id'], row['name'], row['distance'], row['moving_time'], row['elapsed_time'],
        row["moving_time_hms"], row["elapsed_time_hms"], row['average_speed'],
        row['speed_minutes_per_km'], row['speed_minutes_per_km_hms'], row['total_elevation_gain'],
        normalize_sport_type(row['sport_type']), row['start_date'], row['start_date_local'],
        row['timezone'], row['achievement_count'], row['kudos_count'], row['gear_id'],
        str(row['start_latlng']), str(row['end_latlng']), row['max_speed'], row['average_cadence'],
        row['average_temp'], row['has_heartrate'], row['average_heartrate'], row['max_heartrate'],
        row['elev_high'], row['elev_low'], row['pr_count'], row['has_kudoed'],
        row['average_watts'], row['kilojoules'], json.dumps(row['map'])
        )
        for _, row in df.iterrows()
    ]

    # Colonnes à insérer
    columns = (
        'id','name', 'distance', 'moving_time', 'elapsed_time','moving_time_hms',
        'elapsed_time_hms', 'average_speed', 'speed_minutes_per_km','speed_minutes_per_km_hms',
        'total_elevation_gain', 'sport_type', 'start_date', 'start_date_local', 'timezone',
        'achievement_count', 'kudos_count', 'gear_id', 'start_latlng', 'end_latlng','max_speed',
        'average_cadence','average_temp', 'has_heartrate', 'average_heartrate', 'max_heartrate',
        'elev_high', 'elev_low', 'pr_count', 'has_kudoed', 'average_watts','kilojoules', 'map'
    )

    for col in columns:
        if col not in df.columns:
            print(f"[DEBUG] Colonne manquante ajoutée: {col}")
            df[col] = None

    insert_query = sql.SQL("""
        INSERT INTO {} ({})
        VALUES %s
        ON CONFLICT (id) DO NOTHING
    """).format(
        sql.Identifier(table_name),
        sql.SQL(', ').join(map(sql.Identifier, columns))
    )

    # Insertion en bulk
    execute_values(cur, insert_query.as_string(conn), values)

    conn.commit()
    cur.close()

    print("Données importées dans PostgreSQL ✅")
