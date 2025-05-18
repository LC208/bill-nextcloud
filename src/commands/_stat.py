from utils.api import CloudClientFactory
import billmgr.misc as misc
from utils.misc import User, from_multiple_get_key, get_stat_measure
from datetime import datetime, date
from pmnextcloud import LOGGER
from utils.consts import DISK_SPACE, DISK_SPACE_DEFAULT, MEASURE_DEFAULT


def stat(module: int) -> None:
    items = misc.get_items_for_sync(module)
    LOGGER.info(f"Items to get stat {items}")
    if items:
        api_client, user_service, group_service = (
            CloudClientFactory.create_client_from_item(next(iter(items)))
        )
        for item in items:
            user = User(item, user_service)
            quota_data = user_service.get_user_data(user.username)["ocs"]["data"][
                "quota"
            ]
            param = from_multiple_get_key(
                misc.itemaddons(item), DISK_SPACE, DISK_SPACE_DEFAULT[1]
            )
            stat_measure = get_stat_measure(item)
            quota_to_stat = 0
            try:
                quota_to_stat = int(quota_data["used"]) * misc.get_relation(
                    MEASURE_DEFAULT, stat_measure
                )
            except Exception as e:
                LOGGER.error(f"Can't get quota with error: {e}")
            misc.insert_stat(item, datetime.now(), param, quota_to_stat, stat_measure)

    misc.poststat(module, date.today())
