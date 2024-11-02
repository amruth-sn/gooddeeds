import pyodbc

connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:gooddeed6969.database.windows.net,1433;"
    "Database=GoodDeed;"
    "UID=mubinmodi@gooddeed6969;"
    "PWD={Cjwl@134};"  # Make sure to URL-encode special characters if necessary
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

try:
    with pyodbc.connect(connection_string) as conn:
        print("Connection successful!")
except Exception as e:
    print("Connection failed:", e)