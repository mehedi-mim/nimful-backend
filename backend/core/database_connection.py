from db import get_session, models
from sqlalchemy import select, func


async def database_health_check():
    async with get_session() as database:
        try:
            user_table_sql = select(models.User)
            data = (await database.execute(user_table_sql)).scalars().first()
            print("Database Connected!")
        except Exception as e:
            print("Database connection error:", e)
