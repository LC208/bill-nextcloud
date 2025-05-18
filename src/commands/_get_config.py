import billmgr.misc as misc
from utils.api import CloudClientFactory
from utils.consts import PICKLE_PATH
from pmnextcloud import LOGGER


def get_config(module: int) -> None:
    _, _, group_service = CloudClientFactory.create_client_from_module(module)
    groups = group_service.get_groups()
    if isinstance(groups, str):
        groups = [groups]
    usergroups = [""] + groups
    LOGGER.info(f"Pickle preset for module {module}")
    misc.pickle(PICKLE_PATH + f"/module_preset_{module}", usergroups)
