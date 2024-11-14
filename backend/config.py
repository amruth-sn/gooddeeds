import os
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
class Config:
    load_dotenv()
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 2,
        'pool_timeout': 30,
        'pool_recycle': 1800,
        'pool_pre_ping': True
    }
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")

    