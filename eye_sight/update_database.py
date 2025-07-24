from eye_sight.strava.fetch_strava import fetch_activities
from eye_sight.strava.clean_data import clean_activities
from eye_sight.params import *
from sqlalchemy import create_engine

def get_existing_activity_ids(engine):
    query = "SELECT id FROM activities"
    with engine.connect() as conn:
        result = conn.execute(query)
        return set(row[0] for row in result.fetchall())

def update_activities():
    engine = create_engine(DB_URI)

    existing_ids = get_existing_activity_ids(engine)
    raw_df = fetch_activities()
    clean_df = clean_activities(raw_df)

    new_df = clean_df[~clean_df["id"].isin(existing_ids)]

    if not new_df.empty:
        new_df.to_sql("activities", con=engine, if_exists="append", index=False)
        print(f"{len(new_df)} nouvelles activités ajoutées.")
    else:
        print("Pas de nouvelles activités.")

if __name__ == "__main__":
    update_activities()
