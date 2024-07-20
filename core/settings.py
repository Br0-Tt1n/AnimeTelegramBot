from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class Settings:
    bots: Bots


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("BOT_TOKEN"),
            admin_id=env.int("ADMIN_ID")
        )
    )


settings = get_settings('.env')


@dataclass
class DatabaseSetting:
    host: str
    user: str
    password: str


@dataclass
class SettingsDB:
    datadb: DatabaseSetting


def get_settings_db(path: str):
    env = Env()
    env.read_env(path)

    return SettingsDB(
        datadb=DatabaseSetting(
            host=env.str("HOST"),
            user=env.str("USER"),
            password=env.str("PASSWORD")
        )
    )


settings_bd = get_settings_db('.env')
