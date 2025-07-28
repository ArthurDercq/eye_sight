from eye_sight.strava.fetch_strava import update_strava_data
from eye_sight.strava.clean_data import clean_data
from eye_sight.params import *
from sqlalchemy import create_engine, inspect, text


def get_existing_activity_ids(engine):
    query = "SELECT id FROM dashboard"
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return set(row[0] for row in result.fetchall())




def check_schema_compatibility(engine, df, table_name="dashboard"):
    inspector = inspect(engine)
    columns_in_db = [col["name"] for col in inspector.get_columns(table_name)]

    # Inclure l'index (ici 'id') dans la liste des colonnes du DataFrame
    columns_in_df = list(df.columns)
    if df.index.name:
        columns_in_df.append(df.index.name)

    missing_in_df = [col for col in columns_in_db if col not in columns_in_df]
    extra_in_df = [col for col in columns_in_df if col not in columns_in_db]

    if missing_in_df or extra_in_df:
        print("❗️Attention : Différence de schéma détectée")
        if missing_in_df:
            print("Colonnes manquantes dans le DataFrame :", missing_in_df)
        if extra_in_df:
            print("Colonnes présentes dans le DataFrame mais pas dans la DB :", extra_in_df)
        return False

    return True




def update_activities():
    engine = create_engine(DB_URI)

    existing_ids = get_existing_activity_ids(engine)

    raw_df = update_strava_data()
    new_data_clean = clean_data(raw_df)

    if new_data_clean.index.name != 'id':
        new_data_clean = new_data_clean.set_index('id')

    new_df = new_data_clean.loc[~new_data_clean.index.isin(existing_ids)]

    if not new_df.empty:
        # Vérifier la compatibilité du schéma
        if not check_schema_compatibility(engine, new_df, table_name="dashboard"):
            print("🚫 Mise à jour annulée : schéma incompatible.")
            return

        # Récupérer l'ordre des colonnes dans la DB
        inspector = inspect(engine)
        columns_in_db = [col["name"] for col in inspector.get_columns("dashboard")]

        # Si 'id' est l'index, il faut gérer son insertion comme colonne séparée
        # Ajouter l'index (id) à la DataFrame comme colonne pour correspondre à la table
        new_df = new_df.reset_index()

        # Réordonner les colonnes de la DataFrame pour qu’elles correspondent à l’ordre en DB
        new_df = new_df[columns_in_db]

        # Insérer les données en base
        new_df.to_sql("dashboard", con=engine, if_exists="append", index=False)
        print(f"{len(new_df)} nouvelles activités ajoutées.")
    else:
        print("Pas de nouvelles activités.")


if __name__ == "__main__":

    update_activities()
