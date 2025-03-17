from utils.api import NextCloudAPIClient, NextCloudUserService
import billmgr.misc as misc
from utils.misc import User


def close(item: int) -> None:
    api_client = NextCloudAPIClient.from_item(item)
    user_service = NextCloudUserService(api_client)

    user = User(item, user_service)
    user_service.delete_user(user.username)

    misc.postclose(item)
