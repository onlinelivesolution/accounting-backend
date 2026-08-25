import pyodbc

SERVER = "DESKTOP-BMKMV1T\SQLEXPRESS"
USER = "sa"
PASSWORD = "abcd123!"
DRIVER = "ODBC Driver 18 for SQL Server"


def get_master_connection():
    return pyodbc.connect(
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"UID={USER};"
        f"PWD={PASSWORD};"
        "TrustServerCertificate=yes;"
    )


async def create_tenant_database(email: str) -> str:
    db_name = f"{email.replace('@', '_').replace('.', '_')}"

    conn = get_master_connection()
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE {db_name}")

    cursor.close()
    conn.close()

    return db_name
