import billmgr.db as db
import billmgr.misc as misc
import secrets
import string
from utils.consts import DISK_SPACE, DISK_SPACE_DEFAULT, MEASURE_DEFAULT  # MEASURE_DICT
from pmnextcloud import LOGGER


def get_measures_from(intname: str):
    measures_relations = [intname]
    ans = db.db_query(
        "SELECT m1.intname FROM measure m1 "
        "WHERE m1.lessmeasure = (SELECT id FROM measure WHERE intname = %s)",
        intname,
    )

    while ans:
        new_names = []
        for cur_lm in ans:
            measures_relations.append(cur_lm["intname"])
            new_names.append(cur_lm["intname"])

        if not new_names:
            break
        placeholders = ", ".join(["%s"] * len(new_names))
        ans = db.db_query(
            "SELECT m1.intname FROM measure m1 "
            f"WHERE m1.lessmeasure IN (SELECT id FROM measure WHERE intname IN ({placeholders}))",
            *new_names,
        )

    return measures_relations


def get_stat_measure(item: int):
    pricelist_params = misc.get_pricelist_params(misc.iteminfo(item)["pricelist"])
    return pricelist_params.get("stat_measure", MEASURE_DEFAULT)


def from_multiple_get_key(params, keys, default):
    for key in keys:
        if key in params:
            return key
    return default


def from_multiple_keys(params, keys, default):
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
    def __init__(self, item, service):
        self.item = item
        self.service = service
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
        quota = from_multiple_keys(
            misc.itemaddons(self.item), DISK_SPACE, DISK_SPACE_DEFAULT
        )
        return int(quota[0]) * misc.get_relation(quota[1], MEASURE_DEFAULT)

    def get_usergroup(self):
        pricelist_params = misc.get_pricelist_params(
            misc.iteminfo(self.item)["pricelist"]
        )
        return pricelist_params.get("usergroup", "")

    def get_last_usergroup(self):
        pricelist_params = misc.get_pricelist_params(
            misc.iteminfo(self.item)["lastpricelist"]
        )
        return pricelist_params.get("usergroup", "")

    def check_if_exists(self):
        return self.username in self.service.get_users(search=self.username)
