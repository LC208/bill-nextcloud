from utils.api import CloudClientFactory
import billmgr.misc as misc
from utils.misc import User
from billmgr.exception import XmlException
from pmnextcloud import LOGGER


def close(item: int) -> None:
    api_client, user_service, group_service = (
        CloudClientFactory.create_client_from_item(item)
    )
    try:
        user = User(item, user_service)
        user_service.delete_user(user.username)
    except Exception as e:
        LOGGER.error("Can't delete user account")
        raise XmlException(f"close_error: {e}") from e
    else:
        misc.postclose(item)
