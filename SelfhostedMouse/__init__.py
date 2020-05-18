#!/usr/bin/env python
# -*- coding: utf-8 -*-
from luckydonaldUtils.logger import logging
from SelfhostedMouse.sockwebserver import create_server
from SelfhostedMouse.mouse import mouse
import asyncio

__author__ = 'luckydonald'
logger = logging.getLogger(__name__)

BIND_HOST = '0.0.0.0'
BIND_PORT = 8080

logging.add_colored_handler(__name__, level=logging.DEBUG)

loop = asyncio.get_event_loop()
logger.debug(f'registering sockwebserver on port {BIND_PORT}')

loop.run_until_complete(create_server(mouse, BIND_HOST, BIND_PORT))
loop.run_forever()
