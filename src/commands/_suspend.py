from utils.api import NextCloudAPI
import billmgr.misc as misc
from pmnextcloud import LOGGER


def suspend(item: int) -> None:
    api = NextCloudAPI.from_item(item)
    if api.suspend_user(f"user_{item}") is None:
        LOGGER.error("Can't disable user in NextCloud")
        raise Exception("Error on Nextcloud side")
    misc.postsuspend(item)
