import billmgr.misc as misc
import requests
from pmnextcloud import LOGGER
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse


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
        return NextCloudAPI(urlparse(base_url).netloc, username, password)

    def _request(self, method, endpoint, params=None, data=None):
        """Метод для выполнения запросов к API NextCloud"""
        url = f"{self.base_url}/ocs/v2.php/cloud/{endpoint}"
        headers = {
            "OCS-APIRequest": "true",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.request(
            method, url, headers=headers, auth=self.auth, params=params, data=data
        )

        if response.status_code == 200:
            return response.json()
        else:
            LOGGER.error(f"Error: {response.status_code}, {response.text}")
            return None

    def create_user(self, username, password, email, groups, quota):
        """Создание нового пользователя"""
        endpoint = "users"
        data = {
            "userid": username,
            "password": password,
            "email": email,
            "groups": groups,
            "quota": quota,
        }
        return self._request("POST", endpoint, data=data)

    def get_users(self):
        """Создание нового пользователя"""
        endpoint = "users"
        return self._request("GET", endpoint)
