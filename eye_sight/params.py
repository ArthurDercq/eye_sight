import os
from dotenv import load_dotenv

load_dotenv()

### CONSTANT STRAVA TOKEN ###
auth_url = os.getenv('auth_url')
activites_url = os.getenv('activites_url')

STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
STRAVA_REFRESH_TOKEN = os.getenv('STRAVA_REFRESH_TOKEN')



### DATABSE ###
DB_PATH = os.getenv("./data/strava_activities.csv")


## Postegresql ##

host = os.getenv("host")
database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")

DB_URI = os.getenv("DB_URI")
