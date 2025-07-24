from eye_sight.main import *


#Get data

activities = fetch_strava_data()
activities_clean = clean_data(activities)

#KPIs to display
