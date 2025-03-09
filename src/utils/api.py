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
        LOGGER.info(f"Error: {response.status_code}, {response.text}")
        if response.status_code == 200:
            json = response.json()
        if json["ocs"]["meta"]["statuscode"] == 200:
            return response
        else:
            LOGGER.error(f"Error: {response.status_code}, {response.text}")
            return None

    def create_user(self, username, password, email, quota):
        """Создание нового пользователя"""
        endpoint = "users"
        data = {
            "userid": username,
            "password": password,
            "email": email,
            "quota": quota,
        }
        return self._request("POST", endpoint, data=data)

    def get_users(self):
        """Получить список пользователей"""
        endpoint = "users"
        return self._request("GET", endpoint)
