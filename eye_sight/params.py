import os
from dotenv import load_dotenv

load_dotenv()

### CONSTANT STRAVA TOKEN ###
AUTH_URL = os.getenv('auth_url')
ACTIVITIES_URL = os.getenv('activites_url')

STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_REFRESH_TOKEN = os.getenv('STRAVA_REFRESH_TOKEN')



### DATABSE ###
DB_PATH = os.getenv("./data/strava_activities.csv")


## Postegresql ##

HOST = os.getenv("host")
DATABASE = os.getenv("database")
USER = os.getenv("user")
PASSWORD = os.getenv("password")
PORT = os.getenv("port")

DB_URI = os.getenv("DB_URI")
