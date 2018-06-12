#!/usr/bin/env python
# -*- coding: utf-8 -*-
from luckydonaldUtils.logger import logging

from SelfhostedMouse.webserver import web_socket, web_server
from SelfhostedMouse.mouse import mouse

BIND_IP = '0.0.0.0'

__author__ = 'luckydonald'
logger = logging.getLogger(__name__)
logging.add_colored_handler(level=logging.DEBUG)



# WS server that sends messages at random intervals
import asyncio
import websockets



def handle_read(loop, conn, waiter):
    req = conn.recv(1024)
    loop.remove_reader(conn.fileno())
    waiter.set_result(req)


sock = web_socket(BIND_IP, 8080)
loop = asyncio.get_event_loop()
logger.debug('registering web_server')
loop.create_task(web_server(loop, sock))
try:
    loop.run_until_complete(websockets.serve(mouse, BIND_IP, 6789))
finally:
    loop.run_forever()
    loop.close()
# end def



#asyncio.get_event_loop().run_until_complete(
#    websockets.serve(mouse, 'localhost', 6789))
#asyncio.get_event_loop().run_forever()