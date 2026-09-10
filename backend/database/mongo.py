from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()


client = MongoClient(
    os.getenv("MONGO_URI")
)


db = client["zavrsni_rad"]


users = db["users"]
predictions = db["predictions"]
analyses = db["analyses"]
notes = db["notes"]
subjects = db["subjects"]

users.create_index("email", unique=True)