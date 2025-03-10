from utils.api import NextCloudAPI
import billmgr.misc as misc
from pmnextcloud import LOGGER


def resume(item: int) -> None:
    api = NextCloudAPI.from_item(item)
    if api.unsuspend_user(f"user_{item}") is None:
        LOGGER.error("Can't disable user in NextCloud")
        raise Exception("Error on Nextcloud side")
    misc.postresume(item)
