import billmgr.db as db
import billmgr.misc as misc
import secrets
import string
from utils.consts import DISK_SPACE, DISK_SPACE_DEFAULT, MEASURE_DEFAULT  # MEASURE_DICT
from pmnextcloud import LOGGER


def from_muliple_keys(params, keys, default):
    for key in keys:
        if key in params:
            return params[key]
    return default


def get_account_id(item):
    item_info = misc.iteminfo(item)
    return item_info["account_id"]


def get_billaccount_email(item):
    acc_id = get_account_id(item)
    return db.db_query(
        "SELECT email FROM user WHERE account=%s ORDER BY id ASC", acc_id
    )[0]["email"]


class User:
    def __init__(self, item, api):
        self.item = item
        self.api = api
        self.username = self.generate_username()
        self.email = self.get_email()
        self.exists = self.check_if_exists()
        if not self.exists:
            self.password = self.generate_password()
        self.quota = self.get_quota()
        self.usergroup = self.get_usergroup()

    def generate_username(self):
        return f"user_{self.item}"

    def get_email(self):
        return get_billaccount_email(self.item)

    def generate_password(self, length=20):
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def get_quota(self):
        quota = from_muliple_keys(
            misc.itemaddons(self.item), DISK_SPACE, DISK_SPACE_DEFAULT
        )
        return int(quota[0]) * misc.get_relation(quota[1], MEASURE_DEFAULT)

    def get_usergroup(self):
        pricelist_params = misc.get_pricelist_params(
            misc.iteminfo(self.item)["pricelist"]
        )
        LOGGER.info(pricelist_params)
        return pricelist_params.get("usergroup", "")

    def check_if_exists(self):
        return self.username in self.api.get_users(search=self.username)


class UserRepository:
    def __init__(self, user):
        self.user = user

    def save_credentials(self):
        misc.save_param(self.user.item, param="username", value=self.user.username)
        if not self.user.exists:
            misc.save_param(
                self.user.item,
                param="userpassword",
                value=self.user.password,
                crypted=True,
            )


class NextCloudService:
    def __init__(self, api):
        self.api = api

    def create_user(self, user):
        if user.exists:
            LOGGER.info(f"User {user.username} already exists in NextCloud")
            return
        if (
            self.api.create_user(user.username, user.password, user.email, user.quota)
            is None
        ):
            LOGGER.error("Can't create user in NextCloud")
            raise Exception("Error on Nextcloud side")

    def setup_usergroup(self, user):
        if user.usergroup not in self.api.get_groups(search=user.usergroup):
            self.api.create_group(user.usergroup)
        self.api.add_user_to_group(user.username, user.usergroup)

    def delete_user(self, user):
        if not user.exists:
            LOGGER.info(f"User {user.username} does not exist in NextCloud")
            return
        if self.api.delete_user(user.username) is None:
            LOGGER.error("Can't delete user in NextCloud")
            raise Exception("Error on Nextcloud side")

    def resume_user(self, user):
        if not user.exists:
            LOGGER.info(f"User {user.username} does not exist in NextCloud")
            return
        if self.api.unsuspend_user(user.username) is None:
            LOGGER.error("Can't enable user in NextCloud")
            raise Exception("Error on Nextcloud side")

    def suspend_user(self, user):
        if not user.exists:
            LOGGER.info(f"User {user.username} does not exist in NextCloud")
            return
        if self.api.suspend_user(user.username) is None:
            LOGGER.error("Can't disable user in NextCloud")
            raise Exception("Error on Nextcloud side")
