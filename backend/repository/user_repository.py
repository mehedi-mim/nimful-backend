from sqlalchemy import select, or_

from db import models, Status


class UserRepository:
    @staticmethod
    async def get_active_user(db, email, username, *args, **kwargs):
        """
        :param db: taking database session
        :param email: checking previous user with this email
        :param username: checking username with this email
        :param args:
        :param kwargs:
        :return: user if exist
        """
        try:
            user_sql = select(models.User).where(
                or_(models.User.email == email, models.User.username == username),
                models.User.status == Status.ACTIVE.value,
            )
            data = (await db.execute(user_sql)).scalars().first()
            return data
        except Exception as e:
            print("Database connection error:", e)

    @staticmethod
    async def get_inactive_user(db, email):
        sql = select(models.User).where(
            models.User.email == email,
            models.User.status == Status.INACTIVE.value
        )
        db_previous_user = (await db.execute(sql)).scalars().first()
        return db_previous_user

    @staticmethod
    async def create_new_user(db, signup_data):
        try:
            db_user = models.User(
                username=signup_data.username,
                email=signup_data.email,
                password_hash=signup_data.password,
                first_name=signup_data.first_name,
                last_name=signup_data.last_name,
                status=Status.INACTIVE.value,
                mobile=signup_data.mobile,
            )
            db.add(db_user)
            await db.commit()
            return db_user
        except Exception as e:
            print(e)

    @staticmethod
    async def get_user_by_id(db, user_id):
        sql = select(models.User).where(
            models.User.id == user_id,
            models.User.status == Status.INACTIVE.value,
            models.User.deleted_at == None
        )
        current_user = (await db.execute(sql)).scalars().first()
        return current_user

    @staticmethod
    async def update_after_verification(db, user):
        user.status = Status.ACTIVE.value
        db.add(user)
        await db.commit()
        return user

    @staticmethod
    async def get_login_email_user(db, email):
        sql = select(models.User).where(
            models.User.email == email,
            models.User.status == models.Status.ACTIVE.value
        )
        db_user = (await db.execute(sql)).scalars().first()
        return db_user
