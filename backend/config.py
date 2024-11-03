import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://db_owner:tYZ6kchHL5nP@ep-quiet-firefly-a4jwnluc.us-east-1.aws.neon.tech/db?sslmode=require"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = "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"