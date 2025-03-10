from utils.api import NextCloudAPI
import billmgr.misc as misc
from pmnextcloud import LOGGER


def close(item: int) -> None:
    api = NextCloudAPI.from_item(item)
    if api.delete_user(f"user_{item}") is None:
        LOGGER.error("Can't delete user in NextCloud")
        raise Exception("Error on Nextcloud side")
    misc.postclose(item)
