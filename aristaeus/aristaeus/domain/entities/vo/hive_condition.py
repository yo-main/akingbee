from dataclasses import dataclass

TRANSLATIONS = {
    "fr": ("Neuve", "Bon état", "Usagée", "Inutilisable"),
    "en": ("Brand new", "Good state", "Used", "Broken"),
}


@dataclass(frozen=True)
class HiveCondition:
    value: str

    @staticmethod
    def get_defaults(language: str) -> list["HiveCondition"]:
        values = TRANSLATIONS[language]
        return list(map(HiveCondition, values))
