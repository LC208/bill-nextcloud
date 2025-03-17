from utils.api import NextCloudAPIClient, NextCloudUserService, NextCloudGroupService
import billmgr.misc as misc
from utils.misc import (
    User,
    UserRepository,
)
from pmnextcloud import LOGGER


def open(item: int) -> None:
    LOGGER.info("dsadsad")
    api_client = NextCloudAPIClient.from_item(item)
    user_service = NextCloudUserService(api_client)
    group_service = NextCloudGroupService(api_client)

    user = User(item, user_service)

    user_service.create_user(user.username, user.password, user.email, user.quota)
    group_service.add_user_to_group(user.username, user.usergroup)

    repository = UserRepository(user)
    repository.save_credentials()

    misc.postopen(item)
