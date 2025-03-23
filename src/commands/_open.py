from utils.api import CloudClientFactory
import billmgr.misc as misc
from utils.misc import (
    User,
    UserRepository,
)
from pmnextcloud import LOGGER


def open(item: int) -> None:
    LOGGER.info("dsadsad")
    api_client, user_service, group_service = (
        CloudClientFactory.create_client_from_item(item)
    )

    user = User(item, user_service)

    user_service.create_user(user.username, user.password, user.email, user.quota)
    group_service.add_user_to_group(user.username, user.usergroup)

    repository = UserRepository(user)
    misc.save_param(item, param="url", value=api_client.base_url)
    repository.save_credentials()

    misc.postopen(item)
