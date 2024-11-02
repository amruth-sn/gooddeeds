import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://db_owner:tYZ6kchHL5nP@ep-quiet-firefly-a4jwnluc.us-east-1.aws.neon.tech/db?sslmode=require"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False