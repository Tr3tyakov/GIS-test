from dynaconf import settings as config

config.configure(
    ENVVAR_PREFIX_FOR_DYNACONF=False,
    load_dotenv=True,  # Это важно для загрузки .env файла
)
settings = config

MIGRATION_URL = "postgresql://{username}:{password}@{host}:{port}/{database}".format(
    username=settings.POSTGRES.user,
    password=settings.POSTGRES.password,
    host=settings.POSTGRES.host,
    port=settings.POSTGRES.port,
    database=settings.POSTGRES.database,
)


DB_URL = "postgresql+{driver}://{username}:{password}@{host}:{port}/{database}".format(
    username=settings.POSTGRES.user,
    password=settings.POSTGRES.password,
    host=settings.POSTGRES.host,
    port=settings.POSTGRES.port,
    database=settings.POSTGRES.database,
    driver=settings.POSTGRES.driver,
)
