from utils.api import NextCloudAPIClient, NextCloudUserService
import billmgr.misc as misc
from utils.misc import User


def suspend(item: int) -> None:
    api_client = NextCloudAPIClient.from_item(item)
    user_service = NextCloudUserService(api_client)

    user = User(item, user_service)

    user_service.suspend_user(user.username)
    misc.postsuspend(item)
