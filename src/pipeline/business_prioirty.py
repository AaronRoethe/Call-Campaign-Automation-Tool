import json
import os
from dataclasses import dataclass

from .tables import CONFIG_PATH
from .utils import Business_Days

bus_day = Business_Days()


@dataclass
class Business_Line:
    pass

    def as_dict(self):
        pass


def read_json(name):
    with open(CONFIG_PATH / name) as json_file:
        return json.load(json_file)


def write_json(output):
    with open(CONFIG_PATH / f"{bus_day.today_str}.json", "w") as file:
        json.dump(output, file, indent=4)


def company_busines_lines() -> list[Business_Line]:
    try:
        custom_skills = os.listdir(CONFIG_PATH / "custom_skills")
        data = read_json(f"custom_skills/{max(custom_skills)}")
        new_skill = Business_Line()
        bus = [Business_Line(*d.values()) for d in data]
        bus.append(new_skill)
        return bus
    except:
        return None
