import requests
from app import db, app
from models import DaysOfWeek, Equipment, Exercise

db.drop_all()
db.create_all()

#####
# Pull Days of Week data from API
#####
days_data = requests.get("https://wger.de/api/v2/daysofweek/?format=json").json()
days_of_week = [DaysOfWeek(days_of_week=days["day_of_week"].lower()) for days in days_data["results"]]

db.session.add_all(days_of_week)

#####
# Pull Equipment data from API
#####
equip_data = requests.get("https://wger.de/api/v2/equipment/?format=json").json()
equipment_id = [Equipment(id=equip_id["id"]) for equip_id in equip_data["results"]]
equipment_name = [Equipment(name=equip_name["name"].lower()) for equip_name in equip_data["results"]]

db.session.add_all(equipment_id)
db.session.add_all(equipment_name)

#####
# Pull Excercise data from API
#####
exerc_data = requests.get("https://wger.de/api/v2/exercise/?format=json").json()
exercise_id = [Exercise(id=exerc_name["id"]) for exerc_name in exerc_data["results"]]
exercise_name = [Exercise(name=exerc_name["name"].lower()) for exerc_name in exerc_data["results"]]
exercise_description = [Exercise(name=exerc_description["description"].lower()) for exerc_description in exerc_data["results"]]

db.session.add_all(exercise_id)
db.session.add_all(exercise_name)


db.session.commit()