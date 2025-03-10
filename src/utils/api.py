import billmgr.misc as misc
import requests
from pmnextcloud import LOGGER
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse
from utils.consts import API_VERSION
import xml.etree.ElementTree as ET


class NextCloudAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.auth = HTTPBasicAuth(self.username, self.password)

    def from_item(item):
        """Метод создаёт объект API из кода услуги"""
        processingmodule_id = misc.get_item_processingmodule(item)
        proccesingparam = misc.get_module_params(processingmodule_id)
        base_url = proccesingparam["base_url"]
        username = proccesingparam["nc_username"]
        password = proccesingparam["nc_password"]
        return NextCloudAPI(
            f"{urlparse(base_url).scheme}://{urlparse(base_url).netloc}",
            username,
            password,
        )

    def _request(self, method, endpoint, params=None, data=None):
        """Метод для выполнения запросов к API NextCloud"""
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
        else:
            return None

    def create_user(self, username: str, password: str, email: str, quota: int):
        """Создание нового пользователя"""
        endpoint = "users"
        data = {
            "userid": username,
            "password": password,
            "email": email,
            "quota": quota,
        }
        return self._request("POST", endpoint, data=data)

    def get_groups(self, search=None, limit=None, offset=None):
        """Получение списка групп с возможностью фильтрации и пагинации"""
        endpoint = f"groups"
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
        endpoint = f"groups"
        data = {
            "groupid": groupid,
        }
        return self._request("POST", endpoint, data=data)

    def add_user_to_group(self, userid: str, groupid: str):
        endpoint = f"users/{userid}/groups"
        data = {
            "groupid": groupid,
        }
        return self._request("POST", endpoint, data=data)

    def suspend_user(self, userid: str):
        endpoint = f"users/{userid}/disable"
        return self._request("PUT", endpoint)

    def unsuspend_user(self, userid: str):
        endpoint = f"users/{userid}/enable"
        return self._request("PUT", endpoint)

    def get_users(self, search=None, limit=None, offset=None):
        """Получение списка пользователей с возможностью фильтрации и пагинации"""
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
