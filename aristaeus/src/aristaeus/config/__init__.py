from dynaconf import Dynaconf  # type: ignore

settings = Dynaconf(
    envvar_prefix="AKB",
    settings_files=["config.toml", ".secrets.toml"],
    environments=True,
    load_dotenv=True,
    env_switcher="AKB_ENV",
)
