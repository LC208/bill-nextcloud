#!/usr/bin/python3
"""
    Точка входа в программу
"""
import sys

sys.path.append("/usr/local/mgr5/lib/python")
from billmgr.modules.processing import ProcessingModule, Feature
from billmgr.exception import XmlException
import billmgr.logger as logging
import utils.consts as Params
import commands as cmd
from typing import Dict

logging.init_logging("pmnextcloud")
LOGGER = logging.get_logger("pmnextcloud")


class NextcloudModule(ProcessingModule):
    """
    Реализация billmgr.modules.processing.ProcessingModule
    """

    def __init__(self) -> None:
        super().__init__(itemtypes=Params.ITEMTYPE)
        self.add_argument("--password", type=str, help="userpassword", dest="password")
        self.add_argument("--userid", type=str, help="userid", dest="user_id")
        self.add_argument("--subcommand", type=str, help="subaction", dest="action")
        self.add_argument("--itemtype", type=str, help="itemtype", dest="itemtype")
        self.set_description("Модуль для панели Nextcloud")

        self._add_callable_feature(
            Feature.CHECK_CONNECTION, cmd.import_func("check_connection")
        )
        self._add_callable_feature(Feature.OPEN, cmd.import_func("open"))
        self._add_callable_feature(Feature.CLOSE, cmd.import_func("close"))
        self._add_callable_feature(Feature.RESUME, cmd.import_func("resume"))
        self._add_callable_feature(Feature.SUSPEND, cmd.import_func("suspend"))
        self._add_callable_feature(Feature.SET_PARAM, cmd.import_func("set_param"))
        self._add_feature(Feature.PRICELIST_DYNAMIC_SETTINGS)
        # self._add_callable_feature(
        #     Feature.PRICELIST_DYNAMIC_SETTINGS_TUNE,
        #     cmd.import_func("pricelist_dynamic_settings_tune"),
        # )
        # self._add_callable_feature(ExFeature.STAT, cmd.import_func("set_param"))
        # self._add_callable_feature(
        #     Feature.TRANSITION_CONTROL_PANEL, cmd.import_func('transition_control_panel')
        # )

    def get_module_param(self) -> Dict[str, Dict[str, str]]:
        """
        Возвращает набор обязательных параметров,
        которые необходимы при настройке обработчика.
        """
        return {"base_url": {}, "nc_username": {}, "nc_password": {}}

    def _on_raise_exception(self, args, err: XmlException) -> None:
        super()._on_raise_exception(args, err)
        LOGGER.extinfo(args)
        sys.stdout.write(err.as_xml())


if __name__ == "__main__":
    LOGGER.extinfo(sys.argv)
    NextcloudModule().run()
