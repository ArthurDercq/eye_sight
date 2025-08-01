import os
from dotenv import load_dotenv

load_dotenv()

### CONSTANT STRAVA TOKEN ###
AUTH_URL = os.getenv('AUTH_URL')
ACTIVITES_URL = os.getenv('ACTIVITES_URL')

STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_REFRESH_TOKEN = os.getenv('STRAVA_REFRESH_TOKEN')



### DATABSE ###
DB_PATH = os.getenv("./data/strava_activities.csv")


## Postegresql ##

HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")

DB_URI = os.getenv("DB_URI")
