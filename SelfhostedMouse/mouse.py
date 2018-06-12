# -*- coding: utf-8 -*-
import json
import platform

import websockets
from base64 import decodebytes
from pynput.mouse import Controller, Button
from .luckydonald_clipboard.clipboard_mac import Clipboard
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


if platform.system() == 'Darwin':  # Mac OS X
    import Quartz

    def check_postiton(x, y):
        best = False, False
        for i in range(1000):  # if you have more that 1000 displays connected, raise an issue!
            correct_x = correct_y = False
            bounds = Quartz.CGDisplayBounds(i)
            if bounds.origin.x == 0 and bounds.origin.y == 0 and bounds.size.width == 0 and bounds.size.height == 0:
                # we are at the end
                break
            # end if
            if x >= bounds.origin.x and x < bounds.origin.x + bounds.size.width:
                correct_x = True
            # end if
            if y >= bounds.origin.y and y < bounds.origin.y + bounds.size.height:
                correct_y = True
            # end if
            if correct_x and correct_y:
                return True
            # end if
        # end for
        return False
    # end def

    def mouse_move(x,y):
        _x, _y = m.position
        _x_ = _x+x
        _y_ = _y+y

        if check_postiton(_x_, _y_):
            m.position = _x_, _y_
        else:
            logger.debug('Position {x}x{y} would be out of bounds.'.format(x=x, y=y))
        # end if
    # end def
else:
    mouse_move = m.move
# end if


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
                mouse_move(x,y)
            elif data['action'] == 'scroll' and 'x' in data and 'y' in data:
                x, y = int(data['x']), int(data['y'])
                logger.info('scroll - x: {x}, y: {y}'.format(x=x, y=y))
                m.scroll(x,y)
            elif data['action'] == 'paste' and (('text' in data and data['text']) or ('file' in data and data['file'])):
                append = False
                import base64
                if 'file' in data and data['file']:
                    file = data['file']
                    img_data = file['data']
                    del file['data']
                    img_type, img_data = tuple(img_data.split(",", 1))
                    logger.info('got file of type {!r}: {!r}'.format(img_type, file))
                    assert img_type.endswith(';base64');
                    assert img_type.startswith('data:')
                    img_mime = img_type[5:-7]
                    img_data = base64.b64decode(img_data)
                    Clipboard().copy_img(img_data, mime=img_mime)
                    append = True
                # end if
                if 'text' in data and data['text']:
                    Clipboard().copy_text(data['text'], clear_first=not append)
                # end if
            else:
                logging.error("unsupported event: {!r}".format(data))
            # end if
    except websockets.exceptions.ConnectionClosed:
        logger.info('ConnectionClosed, disconnecting.')
    finally:
        await unregister(websocket)
