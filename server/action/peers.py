#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ast import main
import util.common_util as cmd_util
import util.http_util as http_util
import json

def list():
    result = cmd_util.run_cmd('/var/apps/EasyTier-Lite/target/bin/easytier-cli --output json peer')
    peer_list = json.loads(result)
    http_util.http_response_ok(peer_list)
