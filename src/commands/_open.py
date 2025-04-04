from utils.api import CloudClientFactory
import billmgr.misc as misc
from utils.misc import (
    User,
)
from pmnextcloud import LOGGER


def open(item: int) -> None:
    api_client, user_service, group_service = (
        CloudClientFactory.create_client_from_item(item)
    )
    user = User(item, user_service)
    if user.exists:
        raise billmgr.exception.XmlException("open_colission_error")
    try:
        user_service.create_user(user.username, user.password, user.email, user.quota)
    except:
        LOGGER.error("Can't create user account")
        raise billmgr.exception.XmlException("open_error")
    try:
        group_service.add_user_to_group(user.username, user.usergroup)
        misc.save_param(user.item, param="username", value=user.username)
        if not user.exists:
            misc.save_param(
                user.item,
                param="userpassword",
                value=user.password,
                crypted=True,
            )
        misc.save_param(item, param="url", value=api_client.base_url)
    except:
        LOGGER.error("Can't save user account")
        user_service.delete_user(user.username)
    else:
        misc.postopen(item)
