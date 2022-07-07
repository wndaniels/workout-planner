import this
import requests
from app import db, app
from bs4 import BeautifulSoup
from models import DaysOfWeek, Equipment, Exercise

db.drop_all()
db.create_all()


#####
# Pull Days of Week data from API
#####
days_data = requests.get("https://wger.de/api/v2/daysofweek/?format=json").json()
days_of_week = [DaysOfWeek(days_of_week=days["day_of_week"]) for days in days_data["results"]]

db.session.add_all(days_of_week)
db.session.commit()

#####
# Pull Equipment data from API
#####
newEquipData = []
equip_data = requests.get("https://wger.de/api/v2/equipment/?format=json").json()
for equip in equip_data["results"]:
    newEquipData.append(Equipment(id=equip["id"], name=equip["name"]))

db.session.add_all(newEquipData)
db.session.commit()

#####
# Pull Excercise data from API
#####
newExercData = []
exerc_data = requests.get("https://wger.de/api/v2/exercise/?format=json&limit=231&language=2").json()

for exerc in exerc_data["results"]:
    equip_id = exerc["equipment"][0] if len(exerc["equipment"]) > 0 else 7
    descript = exerc["description"]
    soup = BeautifulSoup(descript, features='html.parser')

    newExercData.append(Exercise(name=exerc["name"], description=soup.get_text(), equipment_id=equip_id))

db.session.add_all(newExercData)
db.session.commit()