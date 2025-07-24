

install_requirements:
	@pip install -r requirements.txt

init:
	python eye_sight/main.py

update:
	python eye_sight/update_database.py

run:
	streamlit run eye_sight/app/app.py
