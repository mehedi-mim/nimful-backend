import datetime
import uuid

from sqlalchemy import select, or_

from db import models, Status


class WebCloudRepository:
    @staticmethod
    async def get_web_cloud_data(
            db,
            user,
            *args,
            **kwargs
    ):
        """

        :param db:
        :param user:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            user_sql = select(models.DomainVisitUser).where(
                models.DomainVisitUser.user_id == user.id,
                models.DomainVisitUser.deleted_at == None
            )
            data = (await db.execute(user_sql)).scalars().first()
            return data
        except Exception as e:
            print("No data found:", e)
            return []

    @staticmethod
    async def delete_data(
            db,
            data,
            *args,
            **kwargs
    ):
        """
        :param db:
        :param data:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            data.deleted_at = datetime.datetime.now()
            db.add(data)
            await db.commit()
            return data
        except Exception as e:
            print("Error while deleting:", e)
        return "Success!"
