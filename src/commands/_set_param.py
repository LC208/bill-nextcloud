from utils.api import CloudClientFactory
import billmgr.misc as misc
from utils.misc import User


def set_param(item: int, user_id: int, runningoperation: int) -> None:
    api_client, user_service, group_service = (
        CloudClientFactory.create_client_from_item(item)
    )

    user = User(item, user_service)
    try:
        if user.usergroup != user.get_last_usergroup():
            group_service.remove_user_from_group(
                user.username, user.get_last_usergroup()
            )
            group_service.add_user_to_group(user.username, user.usergroup)
    except:
        LOGGER.error(
            "Error when trying to change the user group. Please check that the groups in the PM settings exist on the panel."
        )
    try:
        user_service.update_user_quota(user.username, user.quota)
    except:
        LOGGER.error("Can't update quota of user account")
        raise billmgr.exception.XmlException("set_param_error")
    else:
        misc.postsetparam(item)
