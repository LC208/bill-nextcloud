from utils.api import CloudClientFactory
import billmgr.misc as misc
from utils.misc import User


def suspend(item: int) -> None:
    api_client, user_service, group_service = (
        CloudClientFactory.create_client_from_item(item)
    )

    user = User(item, user_service)

    user_service.suspend_user(user.username)
    misc.postsuspend(item)
