from dataclasses import dataclass

TRANSLATIONS = {
    "fr": ("Bonne", "Moyenne", "Mauvaise"),
    "en": ("Good", "Medium", "Bad"),
}


@dataclass(frozen=True)
class SwarmHealth:
    value: str

    @staticmethod
    def get_defaults(language: str) -> list["SwarmHealth"]:
        values = TRANSLATIONS[language]
        return list(map(SwarmHealth, values))
