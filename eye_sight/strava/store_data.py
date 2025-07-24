
import pandas as pd
import sqlite3
import psycopg2
from psycopg2 import sql
from datetime import datetime
from eye_sight.strava.clean_data import *
from eye_sight.strava.fetch_strava import *
from eye_sight.params import *
from datetime import datetime



def store_df_in_csv(df, db_path):

    # Exporter le DataFrame nettoyé en fichier CSV
    df.to_csv(db_path, index=False)

    print("Database sauvegardée en csv ✅")



def store_df_in_sqlite(df, db_path, table_name='activities'):
    #Stocke un DataFrame dans une base de données SQLite
    conn = sqlite3.connect(db_path)
    try:
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data successfully stored in {table_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()



def store_df_in_postgresql(db_path):

    creation_date = datetime.now().strftime('%Y-%m-%d')

    # Lire le fichier CSV dans un DataFrame pandas
    df = pd.read_csv(db_path)

    # Connexion à la base de données PostgreSQL
    # Remplacez les valeurs par vos informations de connexion PostgreSQL
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Créer un curseur pour exécuter des commandes SQL
    cur = conn.cursor()

    # Nom de la table dans laquelle vous allez importer les données
    table_name = f"activities_{datetime}"

    # Créer la table dans PostgreSQL
    # Assurez-vous que les types de données correspondent à ceux de votre CSV
    create_table_query = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {} (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    distance FLOAT,
    moving_time INTEGER,
    elapsed_time INTEGER,
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
    average_speed FLOAT,
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
    kilojoules FLOAT
);
""").format(sql.Identifier(table_name))

    cur.execute(create_table_query)

    # Insérer les données dans la table
    for index, row in df.iterrows():
        insert_query = sql.SQL("""
        INSERT INTO {} (
            name, distance, moving_time, elapsed_time, total_elevation_gain,
            sport_type, start_date, start_date_local, timezone, achievement_count,
            kudos_count, gear_id, start_latlng, end_latlng, average_speed,
            max_speed, average_cadence, average_temp, has_heartrate,
            average_heartrate, max_heartrate, elev_high, elev_low, pr_count,
            has_kudoed, average_watts, kilojoules
        ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
        """).format(sql.Identifier(table_name))

        cur.execute(insert_query, (

        row['name'], row['distance'], row['moving_time'], row['elapsed_time'],
        row['total_elevation_gain'], row['sport_type'], row['start_date'],
        row['start_date_local'], row['timezone'], row['achievement_count'],
        row['kudos_count'], row['gear_id'], str(row['start_latlng']),
        str(row['end_latlng']), row['average_speed'], row['max_speed'],
        row['average_cadence'], row['average_temp'], row['has_heartrate'],
        row['average_heartrate'], row['max_heartrate'], row['elev_high'],
        row['elev_low'], row['pr_count'], row['has_kudoed'],
        row['average_watts'], row['kilojoules']
    ))

    # Valider les changements
    conn.commit()

    # Fermer le curseur et la connexion
    cur.close()
    conn.close()

    print("Données importées dans PostgreSQL ✅")
