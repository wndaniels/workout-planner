import requests
from app import db, app
from models import DaysOfWeek, Equiment, Exercise

db.drop_all()
db.create_all()

days_data = requests.get("https://wger.de/api/v2/daysofweek/?format=json").json()
days_of_week = [DaysOfWeek(days_of_week=days["day_of_week"].lower()) for days in days_data["results"]]

db.session.add_all(days_of_week)

equip_data = requests.get("https://wger.de/api/v2/equipment/?format=json").json()
equipment_id = [Equiment(id=equip_id["id"].lower()) for equip_id in equip_data["results"]]
equipment_name = [Equiment(name=equip_name["name"].lower()) for equip_name in equip_data["results"]]

db.session.add_all(equipment_id, equipment_name)


exerc_data = requests.get("https://wger.de/api/v2/exercise/?format=json").json()
exercise_name = [Exercise(name=exerc_name["name"].lower()) for exerc_name in exerc_data["results"]]

db.session.add_all(exercise_name)
db.session.commit()