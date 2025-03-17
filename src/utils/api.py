import billmgr.misc as misc
import requests
from pmnextcloud import LOGGER
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse
from utils.consts import API_VERSION
from abc import ABC, abstractmethod


class IAPIClient(ABC):
    @abstractmethod
    def request(
        self, method: str, endpoint: str, params: dict = None, data: dict = None
    ):
        pass


class NextCloudAPIClient(IAPIClient):
    """
    Класс для выполнения HTTP-запросов к API NextCloud.
    """

    def __init__(self, base_url: str, username: str, password: str):
        """
        Инициализация API клиента.
        :param base_url: URL NextCloud
        :param username: Имя пользователя
        :param password: Пароль пользователя
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.auth = HTTPBasicAuth(self.username, self.password)

    @staticmethod
    def from_item(item):
        """
        Создаёт объект API из кода услуги.

        :param item: Код услуги
        :return: Экземпляр NextCloudAPIClient
        """
        processingmodule_id = misc.get_item_processingmodule(item)
        processingparam = misc.get_module_params(processingmodule_id)
        base_url = processingparam["base_url"]
        username = processingparam["nc_username"]
        password = processingparam["nc_password"]
        return NextCloudAPIClient(
            f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}",
            username,
            password,
        )

    def request(
        self, method: str, endpoint: str, params: dict = None, data: dict = None
    ):
        """
        Выполняет запрос к API NextCloud.
        :param method: HTTP-метод запроса (GET, POST, PUT, DELETE)
        :param endpoint: Конечная точка API
        :param params: Параметры запроса (опционально)
        :param data: Данные запроса (опционально)
        :return: Ответ API или None в случае ошибки
        """
        url = f"{self.base_url}/ocs/{API_VERSION}.php/cloud/{endpoint}"
        headers = {"OCS-APIRequest": "true", "Accept": "application/json"}
        response = requests.request(
            method, url, headers=headers, auth=self.auth, params=params, data=data
        )
        LOGGER.info(f"{method}, {url}, {response.status_code}, {response.text}")
        if response.status_code == 200:
            json = response.json()
            if json["ocs"]["meta"]["statuscode"] == 200:
                return response
        return None


class IUserService(ABC):
    @abstractmethod
    def create_user(self, userid: str, password: str, email: str, quota: int):
        pass

    @abstractmethod
    def delete_user(self, userid: str):
        pass

    @abstractmethod
    def update_user_quota(self, userid: str, quota: int):
        pass

    @abstractmethod
    def suspend_user(self, userid: str):
        pass

    @abstractmethod
    def resume_user(self, userid: str):
        pass

    @abstractmethod
    def get_users(self, search: str = None, limit: int = None, offset: int = None):
        pass


class GroupService(ABC):
    @abstractmethod
    def create_group(self, groupid: str):
        pass

    @abstractmethod
    def add_user_to_group(self, userid: str, groupid: str):
        pass

    @abstractmethod
    def remove_user_from_group(self, userid: str, groupid: str):
        pass


class NextCloudUserService(IUserService):
    def __init__(self, api: IAPIClient):
        self.api = api

    def create_user(self, userid: str, password: str, email: str, quota: int):
        endpoint = "users"
        data = {"userid": userid, "password": password, "email": email, "quota": quota}
        return self.api.request("POST", endpoint, data=data)

    def delete_user(self, userid: str):
        endpoint = f"users/{userid}"
        return self.api.request("DELETE", endpoint)

    def update_user_quota(self, userid: str, quota: int):
        endpoint = f"users/{userid}"
        data = {"key": "quota", "value": quota}
        return self.api.request("PUT", endpoint, data=data)

    def suspend_user(self, userid: str):
        endpoint = f"users/{userid}/disable"
        return self.api.request("PUT", endpoint)

    def resume_user(self, userid: str):
        endpoint = f"users/{userid}/enable"
        return self.api.request("PUT", endpoint)

    def get_users(self, search: str = None, limit: int = None, offset: int = None):
        """
        Получает список пользователей с возможностью фильтрации и пагинации.

        :param search: Фильтр по имени пользователя (опционально)
        :param limit: Ограничение количества записей (опционально)
        :param offset: Смещение для пагинации (опционально)
        :return: Список пользователей или None в случае ошибки
        """
        endpoint = "users"
        params = {}
        if search is not None:
            params["search"] = search
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        response = self.api.request("GET", endpoint, params=params)
        if response:
            return response.json()["ocs"]["data"]["users"]
        return None


class NextCloudGroupService(GroupService):
    def __init__(self, api: IAPIClient):
        self.api = api

    def create_group(self, groupid: str):
        endpoint = "groups"
        data = {"groupid": groupid}
        return self.api.request("POST", endpoint, data=data)

    def add_user_to_group(self, userid: str, groupid: str):
        endpoint = f"users/{userid}/groups"
        data = {"groupid": groupid}
        return self.api.request("POST", endpoint, data=data)

    def remove_user_from_group(self, userid: str, groupid: str):
        endpoint = f"users/{userid}/groups"
        data = {"groupid": groupid}
        return self.api.request("DELETE", endpoint, data=data)
