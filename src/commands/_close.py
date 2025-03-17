from utils.api import NextCloudAPI
import billmgr.misc as misc
from utils.misc import NextCloudService, User


def close(item: int) -> None:
    api = NextCloudAPI.from_item(item)
    user = User(item, api)
    service = NextCloudService(api)
    service.delete_user(user)
    misc.postclose(item)
