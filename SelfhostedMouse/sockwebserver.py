import asyncio
from http import HTTPStatus

import websockets
from luckydonaldUtils.logger import logging
from luckydonaldUtils.encoding import to_binary as b
from luckydonaldUtils.eastereggs.headers import get_headers
from luckydonaldUtils.eastereggs.quotes import get_quote
logger = logging.getLogger(__name__)


def read_file(file):
    with open(file, 'rb') as f:
        return f.read()
    # end with
# end def


class WebSocketServerProtocol2(websockets.WebSocketServerProtocol):
    """
    Like the normal one, but with a custom process_request, adding extra routing for the main page.
    """
    @asyncio.coroutine
    def process_request(self, path, request_headers):
        """
        Intercept the HTTP request and return an HTTP response if needed.

        ``request_headers`` are a :class:`~http.client.HTTPMessage`.

        If this coroutine returns ``None``, the WebSocket handshake continues.
        If it returns a status code, headers and a optionally a response body,
        that HTTP response is sent and the connection is closed.

        The HTTP status must be a :class:`~http.HTTPStatus`. HTTP headers must
        be an iterable of ``(name, value)`` pairs. If provided, the HTTP
        response body must be :class:`bytes`.

        (:class:`~http.HTTPStatus` was added in Python 3.5. Use a compatible
        object on earlier versions. Look at ``SWITCHING_PROTOCOLS`` in
        ``websockets.compatibility`` for an example.)

        This method may be overridden to check the request headers and set a
        different status, for example to authenticate the request and return
        ``HTTPStatus.UNAUTHORIZED`` or ``HTTPStatus.FORBIDDEN``.

        It is declared as a coroutine because such authentication checks are
        likely to require network requests.

        """
        status_code = HTTPStatus(200)
        headers = get_headers()
        body = b''
        if path == "/":  # main page
            body = read_file('./static/index.html')
            headers['Content-type'] = 'text/html'
        elif path == '/pp.js':
            body = read_file('./static/prettyprint.js')
            headers['Content-type'] = 'text/javascript'
        elif path == '/s':  # socket
            return None
        else:
            body = "`" + get_quote('en') + "`\n\n" \
                   "The requested page was not found. Probably somebody broke something."
            status_code = HTTPStatus(404)
        return status_code, headers.items(), b(body)
    # end def

# end class


def create_server(ws_handler, host='0.0.0.0', port=8080, **serve_kwargs):
    serve_kwargs['host'] = host
    serve_kwargs['port'] = port
    serve_kwargs['create_protocol'] = WebSocketServerProtocol2
    return websockets.serve(ws_handler, **serve_kwargs)
# end def


if __name__ == '__main__':
    async def test(websocket, path):
        logger.debug("{!r}, {!r}".format(websocket, path))
    # end def

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(create_server(test))
    finally:
        loop.run_forever()
        loop.close()
    # end def
# end if
