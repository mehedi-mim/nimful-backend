import datetime
import json
import uuid

from sqlalchemy import select, or_

from db import models, Status


class UserRepository:
    @staticmethod
    async def get_previous_email_or_username_check(db, email, username, *args, **kwargs):
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

    @staticmethod
    async def verify_seed_data(db, seed):
        sql = select(models.User).where(
            models.User.seed == seed,
            models.User.status == models.Status.ACTIVE.value
        )
        db_user = (await db.execute(sql)).scalars().first()
        await db.close()
        return db_user

    @staticmethod
    async def create_seed_data(db, current_user):
        try:
            seed = uuid.uuid4().hex
            current_user.seed = seed
            db.add(current_user)
            await db.commit()
            return current_user
        except Exception as e:
            return None

    @staticmethod
    async def check_previous_data(db, user):
        today = datetime.datetime.today().date()
        sql = select(models.DomainVisitUser).where(
            models.DomainVisitUser.user_id == user.id,
            models.DomainVisitUser.deleted_at == None
        )
        db_domain_visit = (await db.execute(sql)).scalars().first()
        return db_domain_visit

    @staticmethod
    async def create_domain_visit_user(db, data, user, seed_domain):
        if data is not None:
            json_data = json.loads(data.domain_visits)
            previous_count = json_data.get(f"{seed_domain.domain}", 0)
            json_data[f"{seed_domain.domain}"] = previous_count + 1
            data.domain_visits = json.dumps(json_data)
            db.add(data)
            await db.commit()
            await db.close()
            return data
        print("New row created...!")
        json_data = {
            f"{seed_domain.domain}": 1
        }
        db_domain_visit = models.DomainVisitUser(
            user_id=user.id,
            domain_visits=json.dumps(json_data)
        )
        db.add(db_domain_visit)
        await db.commit()
        return db_domain_visit
