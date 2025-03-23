from utils.api import CloudClientFactory
import billmgr.misc as misc
from utils.misc import User


def close(item: int) -> None:
    api_client, user_service, group_service = (
        CloudClientFactory.create_client_from_item(item)
    )

    user = User(item, user_service)
    user_service.delete_user(user.username)

    misc.postclose(item)
