

install_requirements:
	@pip install -r requirements.txt

create:
	python eye_sight/create_database.py

update:
	python eye_sight/update_database.py

store_csv:
	python eye_sight/strava/store_csv.py

run:
	streamlit run eye_sight/app/app.py
