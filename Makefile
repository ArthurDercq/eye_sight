

install_requirements:
	@pip install -r requirements.txt

init:
	python eye_sight/main.py

update:
	python eye_sight/update_database.py

store_csv:
	python eye_sight/strava/store_csv.py

run:
	streamlit run eye_sight/app/app.py
