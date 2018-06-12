# -*- coding: utf-8 -*-
from luckydonaldUtils.logger import logging

__author__ = 'luckydonald'
logger = logging.getLogger(__name__)


async def web_handler(loop, conn):
    req = await loop.sock_recv(conn, 1024)
    if req:
        head  = b'HTTP/1.1 200 OK\r\n'
        head += b'Content-type: text/html\r\n'
        head += b'\r\n'

        body = await web_read_file('./index.html')

        resp = head + body

        await loop.sock_sendall(conn, resp)
    # end if
    conn.close()
# end def


async def web_server(loop, sock):
    while True:
        logger.debug('ws server started.')
        conn, addr = await loop.sock_accept(sock)
        loop.create_task(web_handler(loop, conn))
    # end while

async def web_read_file(file_):
     with open(file_, 'rb') as f:
        return f.read()
     # end with
# end def

def web_socket(bind_ip="0.0.0.0", bind_port=8080):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(False)
    sock.bind((bind_ip, bind_port))
    sock.listen(10)
    return sock
