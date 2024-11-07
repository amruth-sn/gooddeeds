import os
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
class Config:
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
    MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
    MAILGUN_SANDBOX = os.getenv("MAILGUN_SANDBOX")

    