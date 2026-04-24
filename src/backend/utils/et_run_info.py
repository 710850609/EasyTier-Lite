#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os.path
from pathlib import Path
from typing import Optional, Dict

from utils import run_configs

__data = None

class EtRunInfo:

    def __init__(self, profile:str, rpc_portal:str = None, fn_enabled:bool = False):
        """
        fn_enabled: 仅用于飞牛系统自启控制，其他系统的由系统服务自启控制
        """
        self.profile = profile
        self.rpc_portal = rpc_portal
        self.fn_enabled = fn_enabled

def flag_start(profile:str, rpc_portal:str = None):
    data = __load_profile(profile)
    if data is None:
        data = EtRunInfo(profile, rpc_portal, True)
    data.fn_enabled = True
    __save_profile(data)

def flag_stop(profile:str):
    data = __load_profile(profile)
    if data is None:
        data = EtRunInfo(profile, None, True)
    data.fn_enabled = False
    __save_profile(data)


def __load_profile(profile:str) -> Optional[EtRunInfo]:
    save_data = __load_data() or {}
    return save_data.get(profile, None)

def __save_profile(data:EtRunInfo):
    save_data = __load_data() or {}
    save_data[data.profile] = data
    __save_data(save_data)

def __load_data() -> Dict[str, EtRunInfo]:
    global __data
    if __data is None:
        run_file = run_configs.et_run_file()
        if not os.path.exists(run_file):
            return {}
        with open(run_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for key in data.items():
                data[key] = EtRunInfo(**data[key])
            __data = data
    return __data

def __save_data(data:Dict[str, EtRunInfo]):
    run_file = run_configs.et_run_file()
    if not os.path.exists(run_file):
        Path(run_file).touch()
    with open(run_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)