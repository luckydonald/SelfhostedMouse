# -*- coding: utf-8 -*-
import json
from pynput.mouse import Controller, Button
from luckydonaldUtils.logger import logging

__author__ = 'luckydonald'
logger = logging.getLogger(__name__)

BUTTONS = {
    'left': Button.left, 'right': Button.right, 'middle': Button.middle,
    1: Button.left, 2: Button.right, 3: Button.middle
}

USERS = set()
m = Controller()

async def register(websocket):
    logger.debug('called.')
    USERS.add(websocket)


async def unregister(websocket):
    logger.debug('called.')
    USERS.remove(websocket)


async def mouse(websocket, _):
    # register(websocket) sends user_event() to websocket
    logger.debug('called.')
    await register(websocket)
    try:
        # await websocket.send(state_event())
        async for message in websocket:
            logging.debug('message: {}'.format(message))
            data = json.loads(message)
            if data['action'] == 'click' and 'button' in data and data['button'] in BUTTONS:
                button = data['button']
                logger.info('click - button: {}'.format(button))
                m.click(BUTTONS[button])
            elif data['action'] == 'move' and 'x' in data and 'y' in data:
                x, y = data['x'], data['y']
                logger.info('move - x: {x}, y: {y}'.format(x=y, y=y))
                m.move(x,y)
            elif data['action'] == 'scroll' and 'x' in data and 'y' in data:
                x, y = int(data['x']), int(data['y'])
                logger.info('scroll - x: {x}, y: {y}'.format(x=x, y=y))
                m.scroll(x,y)
            else:
                logging.error("unsupported event: {!r}".format(data))
            # end if
    finally:
        await unregister(websocket)
