from utils.api import NextCloudAPI
import billmgr.misc as misc
from pmnextcloud import LOGGER
from utils.misc import from_muliple_keys, get_billaccount_email
from utils.consts import DISK_SPACE, DISK_SPACE_DEFAULT, MEASURE_DICT, MEASURE_DEFAULT
import secrets
import string


def open(item: int) -> None:
    api = NextCloudAPI.from_item(item)
    email = get_billaccount_email(item)
    username = f"user_{item}"
    alphabet = string.ascii_letters + string.digits
    password = "".join(secrets.choice(alphabet) for i in range(20))
    pricelist_parmas = misc.get_pricelist_params(misc.iteminfo(item)["pricelist"])
    usergroup = ""
    if "usergroup" in pricelist_parmas:
        usergroup = pricelist_parmas["usergroup"]
    quota = from_muliple_keys(misc.itemaddons(item), DISK_SPACE, DISK_SPACE_DEFAULT)
    if (
        api.create_user(
            username,
            password,
            email,
            int(quota[0]) * MEASURE_DICT.get(quota[1], 1),
        )
        is None
    ):
        LOGGER.error("Can't create user in NextCloud")
        raise Exception("Error on Nextcloud side")
    misc.save_param(item, param="username", value=username)
    misc.save_param(item, param="userpassword", value=password, crypted=True)
    misc.postopen(item)
