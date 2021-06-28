from os import environ
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = environ.get("SECRET_KEY",
                         'b9-ct%3wayay6md-9gi=w-r$c^-7ior6@i2*@m^nh-x=yz9xxz')

DEBUG = environ.get("DEBUG", "true") == "true"