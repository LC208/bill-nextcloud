#!/usr/bin/env python3
'''
    Точка входа в программу
'''
import commands as cmd
from enum import Enum
import sys
from typing import Dict
sys.path.insert(0, "/usr/local/mgr5/lib/python")
from billmgr.modules.processing import ProcessingModule, Feature
from billmgr.exception import XmlException
import utils.consts as Params
from utils.logger import logger

class NextcloudModule(ProcessingModule):
    '''
        Реализация billmgr.modules.processing.ProcessingModule
    '''
    def __init__(self) -> None:
        super().__init__(itemtypes=Params.ITEMTYPE)
        self.add_argument("--password", type=str, help="userpassword", dest="password")
        self.add_argument("--userid", type=str, help="userid", dest="user_id")
        self.add_argument("--subcommand", type=str, help="subaction", dest='action')
        self.add_argument("--itemtype", type=str, help="itemtype", dest='itemtype')
        self.set_description("Модуль для панели Nextcloud")

    def get_module_param(self) -> Dict[str, Dict[str, str]]:
        '''
            Возвращает набор обязательных параметров,
            которые необходимы при настройке обработчика.
        '''
        return {
            "base_url": {},
            "nc_username": {},
            "nc_password": {}
        }

    def _on_raise_exception(self, args, err: XmlException) -> None:
        super()._on_raise_exception(args,err)
        logger.extinfo(args)
        sys.stdout.write(err.as_xml())

if __name__ == "__main__":
    logger.extinfo(sys.argv)
    NextcloudModule().run()