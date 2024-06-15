from dataclasses import dataclass

TRANSLATIONS = {
    "fr": ("Planifié", "Retard", "Effectué"),
    "en": ("Planified", "Late", "Done"),
}


@dataclass(frozen=True)
class EventStatus:
    value: str

    @staticmethod
    def get_defaults(language: str) -> list["EventStatus"]:
        values = TRANSLATIONS[language]
        return list(map(EventStatus, values))
