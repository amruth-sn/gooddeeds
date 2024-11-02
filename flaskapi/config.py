from flask import Flask
import os
import pyodbc

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc://mubinmodi%40gooddeed6969:Cjwl@134@gooddeed6969.database.windows.net:1433/GoodDeed?"
        "driver=ODBC+Driver+17+for+SQL+Server;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
        "hostNameInCertificate=*.database.windows.net;"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False