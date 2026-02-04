import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
DATABASE_URL = "mssql+aioodbc://sa:abcd123%21@DESKTOP-GCAJSDB/WorkmationWeb?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"

async def test_connection():
    try:
        engine = create_async_engine(DATABASE_URL, echo=True, future=True)

        async with engine.begin() as conn:
            # ✅ wrap raw SQL in text()
            result = await conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print("✅ Connection successful, query result:", row)

        await engine.dispose()

    except Exception as e:
        print("❌ Connection failed:", str(e))

if __name__ == "__main__":
    asyncio.run(test_connection())