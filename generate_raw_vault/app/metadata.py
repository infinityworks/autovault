from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Dict, Iterable, List, Literal
from pathlib import Path
import json

SQL_TYPES = Literal['STRING', 'INT']

@dataclass_json
@dataclass
class BusinessAttributes:
    business_definition: str
    payload: Dict[str, str]

@dataclass_json
@dataclass
class BusinessTopic:
    business_keys: Dict[str, str]
    business_attributes: List[BusinessAttributes]

@dataclass_json
@dataclass
class Metadata:
    version: int
    source_name: str
    source_system: str
    business_topics: Dict[str, BusinessTopic]

    def satelites(self) -> Iterable[str]:
        for bt in self.business_topics.values():
            yield from (x.business_definition for x in bt.business_attributes)




def load_metadata(path: Path) -> Metadata:
    with open(path, 'r') as in_file:
        data = json.load(in_file)
        return Metadata.from_dict(data)

    
