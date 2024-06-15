from dataclasses import dataclass

EVENT_TYPE_TRANSLATIONS = {
    "fr": ["Bruler les abeilles", "Arroser la ruche", "Trouver une nouvelle ruche", "Trouver une nouvelle reine"],
    "en": ["Burn the bees", "Water the hive", "Find a new hive", "Find a new queen"],
}

EVENT_STATUS_TRANSLATIONS = {
    "fr": ["Planifié", "Fait", "Annulé", "Delayé"],
    "en": ["Planified", "Done", "Cancelled", "Delayed"],
}


@dataclass(frozen=True)
class EventType:
    value: str

    @staticmethod
    def get_defaults(language: str) -> list["EventType"]:
        values = EVENT_TYPE_TRANSLATIONS[language]
        values.extend(EVENT_STATUS_TRANSLATIONS[language])
        return list(map(EventType, values))
