from utils.api import NextCloudAPI
import billmgr.misc as misc
from utils.misc import (
    from_muliple_keys,
    get_billaccount_email,
    NextCloudService,
    User,
    UserRepository,
)


def open(item: int) -> None:
    api = NextCloudAPI.from_item(item)
    user = User(item, api)
    service = NextCloudService(api)
    repository = UserRepository(user)
    service.create_user(user)
    service.setup_usergroup(user)
    repository.save_credentials()
    misc.postopen(item)
