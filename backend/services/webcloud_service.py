import json
from passlib.context import CryptContext
from repository.webcloud_repository import WebCloudRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class WebCloudService(WebCloudRepository):
    async def get_web_cloud(
            self,
            db,
            current_user
    ) -> []:
        """

        :param db:
        :param current_user:
        :return:
        """

        data = await self.get_web_cloud_data(db, current_user)
        if data:
            domain_visits = json.loads(data.domain_visits)
            formatted_data = [{'text': f"{domain} -> {value}", 'value': value * 100} for
                              domain, value in domain_visits.items()]
            return formatted_data
        else:
            return []

    async def clear_history(
            self,
            db,
            current_user
    ) -> str:
        """
        :param db:
        :param current_user:
        :return:
        """

        data = await self.get_web_cloud_data(db, current_user)
        if data:
            return await self.delete_data(db, data)
        else:
            return "Already cleared data!"
