from dataclasses import dataclass

TRANSLATIONS = {
    "fr": ("Toutes fleurs", "Acacia", "Bruyère", "Chataignier", "Tournesol"),
    "en": ("All flowers", "Acacia", "Briar root", "Cheastnut", "Sunflower"),
}


@dataclass(frozen=True, slots=True)
class HoneyType:
    value: str

    @staticmethod
    def get_defaults(language: str) -> list["HoneyType"]:
        values = TRANSLATIONS[language]
        return list(map(HoneyType, values))
