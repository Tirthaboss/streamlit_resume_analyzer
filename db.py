from pymongo import MongoClient
import bcrypt
import os
import streamlit as st
MONGO_URL = st.secrets["MONGO_URL"]  # Use secrets in Streamlit Cloud

client = MongoClient(MONGO_URL)
db = client["resume_app"]
users = db["users"]

def create_user(email, password):
    if users.find_one({"email": email}):
        return False
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users.insert_one({"email": email, "password": hashed})
    return True

def authenticate_user(email, password):
    user = users.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode(), user["password"]):
        return user
    return None

