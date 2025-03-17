from utils.api import NextCloudAPI
import billmgr.misc as misc
from utils.misc import NextCloudService, User


def resume(item: int) -> None:
    api = NextCloudAPI.from_item(item)
    user = User(item, api)
    service = NextCloudService(api)
    service.resume_user(user)
    misc.postresume(item)
