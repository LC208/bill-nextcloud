import billmgr.session as session
import billmgr.misc as misc
from utils.api import NextCloudAPIClient, NextCloudUserService, NextCloudGroupService
import xml.etree.ElementTree as ET
from utils.consts import MEASURE_DEFAULT
from utils.misc import get_measures_from
from pmnextcloud import LOGGER


def pricelist_dynamic_settings_tune(module):
    xml = session.get_input_xml()
    processingparam = misc.get_module_params(module)
    base_url = processingparam["base_url"]
    username = processingparam["nc_username"]
    password = processingparam["nc_password"]
    api = NextCloudAPIClient(base_url, username, password)
    user_service = NextCloudUserService(api)
    group_service = NextCloudGroupService(api)
    groups = group_service.get_groups()
    if isinstance(groups, str):
        groups = [groups]
    usergroups = [""] + groups
    session.make_slist(
        xml,
        "usergroup",
        [
            session.SlistElem(key=usergroup.index(usergroup), name=usergroup)
            for usergroup in usergroups
        ],
    )
    ET.dump(xml)
