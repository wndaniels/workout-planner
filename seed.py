import this
import requests
from app import db, app
from models import DaysOfWeek, Equipment, Exercise

db.drop_all()
db.create_all()


#####
# Pull Days of Week data from API
#####
days_data = requests.get("https://wger.de/api/v2/daysofweek/?format=json").json()
days_of_week = [DaysOfWeek(days_of_week=days["day_of_week"]) for days in days_data["results"]]

db.session.add_all(days_of_week)

#####
# Pull Equipment data from API
#####
newEquipData = []
equip_data = requests.get("https://wger.de/api/v2/equipment/?format=json").json()
for equip in equip_data["results"]:
    newEquipData.append(Equipment(id=equip["id"], name=equip["name"]))

db.session.add_all(newEquipData)

#####
# Pull Excercise data from API
#####
newExercData = []
exerc_data = requests.get("https://wger.de/api/v2/exercise/?format=json&language=2").json()

for exerc in exerc_data["results"]:
    equip_id = exerc["equipment"]
    for equip in range(len(equip_id)):
        newExercData.append(Exercise(name=exerc["name"], description=exerc["description"], equipment_id=(equip_id[equip])))

db.session.add_all(newExercData)


db.session.commit()