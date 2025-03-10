import billmgr.misc as misc
import requests
from pmnextcloud import LOGGER
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse
from utils.consts import API_VERSION
import xml.etree.ElementTree as ET


class NextCloudAPI:
    """
    Класс для взаимодействия с API NextCloud.
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
        :return: Экземпляр NextCloudAPI
        """
        processingmodule_id = misc.get_item_processingmodule(item)
        processingparam = misc.get_module_params(processingmodule_id)
        base_url = processingparam["base_url"]
        username = processingparam["nc_username"]
        password = processingparam["nc_password"]
        return NextCloudAPI(
            f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}",
            username,
            password,
        )

    def _request(
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
        LOGGER.info(f"{response.status_code}, {response.text}")
        if response.status_code == 200:
            json = response.json()
            if json["ocs"]["meta"]["statuscode"] == 200:
                return response
        return None

    def create_user(self, username: str, password: str, email: str, quota: int):
        """
        Создаёт нового пользователя в NextCloud.

        :param username: Имя пользователя
        :param password: Пароль
        :param email: Электронная почта
        :param quota: Квота (размер дискового пространства в мегабайтах)
        :return: Ответ API или None в случае ошибки
        """
        endpoint = "users"
        data = {
            "userid": username,
            "password": password,
            "email": email,
            "quota": quota,
        }
        return self._request("POST", endpoint, data=data)

    def get_groups(self, search: str = None, limit: int = None, offset: int = None):
        """
        Получает список групп с возможностью фильтрации и пагинации.

        :param search: Фильтр по названию группы (опционально)
        :param limit: Ограничение количества записей (опционально)
        :param offset: Смещение для пагинации (опционально)
        :return: Список групп или None в случае ошибки
        """
        endpoint = "groups"
        params = {}
        if search is not None:
            params["search"] = search
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        response = self._request("GET", endpoint, params=params)
        if response:
            return response.json()["ocs"]["data"]["groups"]
        return None

    def create_group(self, groupid: str):
        """
        Создаёт новую группу.

        :param groupid: Идентификатор группы
        :return: Ответ API или None в случае ошибки
        """
        endpoint = "groups"
        data = {"groupid": groupid}
        return self._request("POST", endpoint, data=data)

    def add_user_to_group(self, userid: str, groupid: str):
        """
        Добавляет пользователя в группу.

        :param userid: Идентификатор пользователя
        :param groupid: Идентификатор группы
        :return: Ответ API или None в случае ошибки
        """
        endpoint = f"users/{userid}/groups"
        data = {"groupid": groupid}
        return self._request("POST", endpoint, data=data)

    def suspend_user(self, userid: str):
        """
        Отключает пользователя (замораживает учетную запись).

        :param userid: Идентификатор пользователя
        :return: Ответ API или None в случае ошибки
        """
        endpoint = f"users/{userid}/disable"
        return self._request("PUT", endpoint)

    def unsuspend_user(self, userid: str):
        """
        Разблокирует пользователя (восстанавливает учетную запись).

        :param userid: Идентификатор пользователя
        :return: Ответ API или None в случае ошибки
        """
        endpoint = f"users/{userid}/enable"
        return self._request("PUT", endpoint)

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
        response = self._request("GET", endpoint, params=params)
        if response:
            return response.json()["ocs"]["data"]["users"]
        return None
