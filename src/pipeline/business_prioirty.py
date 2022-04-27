import json
from dataclasses import dataclass, field
from typing import Dict, List

from .tables import CONFIG_PATH

name = 'business_lines.json'
name = 'data.json'

@dataclass
class Business_Line:
    skill: str              = field(default_factory=lambda: "New_skill")
    filters: Dict[str,list] = field(default_factory=lambda:{
                                                            "Audit_Type":[],
                                                            "Project_Type":[],
                                                            "Outreach_Status":[],
                                                            "general":[]
                                                            })
    new_columns: List       = field(default_factory=lambda: [])
    scoring:Dict[str,bool]  = field(default_factory=lambda:{"meet_target_sla":True, 
                                                            "no_call":False,  
                                                            "age":False})

    def as_dict(self):
        return {'skill': self.skill, 'filters': self.filters, 'scoring': self.scoring}

def read_json(name):
    with open(CONFIG_PATH / name) as json_file:
            return json.load(json_file)

def write_json(output):
    with open(CONFIG_PATH / f"test{name}",'w') as file:
        json.dump(output, file, indent=4)

def ciox_busines_lines() -> list[Business_Line]:
    try:
        data = read_json(name)
        new_skill = Business_Line()
        bus = [Business_Line(*d.values()) for d in data]
        bus.append(new_skill)
        return bus
    except:
        return None
