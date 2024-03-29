from pymongo import MongoClient

# import the dotenv_values function
from dotenv import dotenv_values
import os

if os.path.isfile(".env"):
    # Read from the .env file
    config = dotenv_values(".env")
    MONGO_URI = config["MONGO_URI"]

else:
    # Use environmental variables
    MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)  # type: ignore


# connecting to the database
db = client["contact_db"]


# check if the connection is successful
try:
    client.server_info()
    print("Connected to the database")
except Exception as e:
    print(f"Error connecting to the database: {str(e)}")
