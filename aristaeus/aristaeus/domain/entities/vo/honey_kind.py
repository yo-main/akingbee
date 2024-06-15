from dataclasses import dataclass

TRANSLATIONS = {
    "fr": ("Toutes fleurs", "Acacia", "Bruyère", "Chataignier", "Tournesol"),
    "en": ("All flowers", "Acacia", "Briar root", "Cheastnut", "Sunflower"),
}


@dataclass(frozen=True)
class HoneyKind:
    value: str

    @staticmethod
    def get_defaults(language: str) -> list["HoneyKind"]:
        values = TRANSLATIONS[language]
        return list(map(HoneyKind, values))
