from dataclasses import dataclass

TRANSLATIONS = {
    "fr": ("Bruler les abeilles", "Arroser la ruche", "Trouver une nouvelle ruche", "Trouver une nouvelle reine"),
    "en": ("Burn the bees", "Water the hive", "Find a new hive", "Find a new queen"),
}


@dataclass(frozen=True, slots=True)
class EventType:
    value: str

    @staticmethod
    def get_defaults(language: str) -> list["EventType"]:
        values = TRANSLATIONS[language]
        return list(map(EventType, values))
