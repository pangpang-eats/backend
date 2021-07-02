from os import environ
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = environ.get("SECRET_KEY",
                         'b9-ct%3wayay6md-9gi=w-r$c^-7ior6@i2*@m^nh-x=yz9xxz')

DEBUG = environ.get("DEBUG", "true") == "true"

DB_HOST = environ.get("POSTGRES_HOST", "localhost")
DB_PORT = environ.get("POSTGRES_PORT", "5432")
DB_NAME = environ.get("POSTGRES_DB", "postgres")
DB_USER = environ.get("POSTGRES_USER", "postgres")
DB_PASSWORD = environ.get("POSTGRES_PASSWORD", "postgres")