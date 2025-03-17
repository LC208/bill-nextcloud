from utils.api import NextCloudAPIClient, NextCloudUserService, NextCloudGroupService
import billmgr.misc as misc
from utils.misc import User, from_multiple_get_key
from datetime import datetime, date
from pmnextcloud import LOGGER
from utils.consts import DISK_SPACE, DISK_SPACE_DEFAULT, MEASURE_DEFAULT


def stat(module: int) -> None:
    items = misc.get_items_for_sync(module)
    LOGGER.info(f"Item's to get stat {items}")
    if items:
        api = NextCloudAPIClient.from_item(next(iter(items)))
        user_service = NextCloudUserService(api)
        for item in items:
            user = User(item, user_service)
            quota_data = user_service.get_user_data(user.username).json()["ocs"][
                "data"
            ]["quota"]
            param = from_multiple_get_key(
                misc.itemaddons(item), DISK_SPACE, DISK_SPACE_DEFAULT[1]
            )
            misc.insert_stat(
                item, datetime.now(), param, quota_data["used"], MEASURE_DEFAULT
            )

    misc.poststat(module, date.today())
