from utils.api import NextCloudAPI
import billmgr.misc as misc
from utils.misc import (
    from_muliple_keys,
    get_billaccount_email,
    NextCloudService,
    User,
    UserRepository,
)
from pmnextcloud import LOGGER


def set_param(item: int, user_id: int, runningoperation: int) -> None:
    api = NextCloudAPI.from_item(item)
    user = User(item, api)
    service = NextCloudService(api)
    service.update_userparams(user)
    misc.postsetparam(item)
