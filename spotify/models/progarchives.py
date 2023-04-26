from pydantic import BaseModel, Extra
from pydantic.dataclasses import dataclass


class Artist(BaseModel, extra=Extra.ignore):
    name: str
    albums: dict[int, str]

"""
"1": {
        "name": "GENESIS",
        "albums": {
            "2": "FOXTROT",
            "3": "NURSERY CRYME",
            "5": "A TRICK OF THE TAIL",
            "6": "FROM GENESIS TO REVELATION",
            "1510": "SELLING ENGLAND BY THE POUND",
            "1511": "THE LAMB LIES DOWN ON BROADWAY",
            "1512": "WIND & WUTHERING",
            "1515": "...AND THEN THERE WERE THREE...",
            "1516": "DUKE",
            "1517": "ABACAB",
            "1519": "GENESIS",
            "1520": "INVISIBLE TOUCH",
            "1521": "WE CAN'T DANCE",
            "1524": "CALLING ALL STATIONS",
            "2448": "TRESPASS"
        }
    },
}
"""

class Artist(BaseModel, extra=Extra.ignore):
    name: str
    albums: dict[int, str]

"""
"1": {
        "2": "FOXTROT",
        "3": "NURSERY CRYME",
        "5": "A TRICK OF THE TAIL",
        "6": "FROM GENESIS TO REVELATION",
        "1510": "SELLING ENGLAND BY THE POUND",
        "1511": "THE LAMB LIES DOWN ON BROADWAY",
        "1512": "WIND & WUTHERING",
        "1515": "...AND THEN THERE WERE THREE...",
        "1516": "DUKE",
        "1517": "ABACAB",
        "1519": "GENESIS",
        "1520": "INVISIBLE TOUCH",
        "1521": "WE CAN'T DANCE",
        "1524": "CALLING ALL STATIONS",
        "2448": "TRESPASS"
    },
}"""