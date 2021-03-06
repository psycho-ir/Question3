from helpers import _generate_output, _generate_404_output

__author__ = 'soroosh'
import re
import socket
import logging


class Info:
    """
    Some Information about request will wrapped in Info objects
    """

    def __init__(self, ip, headers, opened_port):
        self.opened_port = opened_port
        self.headers = headers
        self.ip = ip


class WebServer:
    """
    Our Webserver engine which has some features like starting and registering actions on it.
    """

    def __init__(self, port, host=''):
        self.host = host
        self.port = port
        self.paused = False
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.actions = []
        self.info = []

    def register_action(self, action):
        """
            You can register actions to handle request
        :param action: from actions.Action object
        :return: void
        """
        self.actions.append(action)

    def start(self):
        """
        Starts webserver
        :return: void
        """
        self._socket.bind((self.host, self.port))
        self._socket.listen(100)
        logging.info("Web Server started on port: %s" % self.port)
        self._run_event_loop()

    def _run_event_loop(self, _generate_500_output=None):
        while not self.paused:
            try:
                sent = False
                csock, caddr = self._socket.accept()
                req = csock.recv(2048)  # 2KB
                logging.info('Request: %s' % req)
                if len(self.actions) == 0:
                    csock.sendall(
                        self._generate_output("<html><body>default</body></html>")
                    )
                self.info.append(Info(caddr[0], req, caddr[1]))
                for action in self.actions:
                    match = re.match(action.regex(), req)
                    if match:
                        m = re.match(r'.*\r\nHost: (.*):.*\r\n', req, re.MULTILINE)
                        if not m:
                            params = []
                            host = ''
                        else:
                            params = match.groups()
                            host = m.group(1)

                        csock.sendall(_generate_output(action.response(request=req, ip=caddr[0], port=caddr[1], params=params, host=host), action.mime_type()))
                        sent = True
                        break
                if not re.match('^GET.*', req):
                    csock.sendall(
                        _generate_500_output("<html><body>Method Not Allowed</body></html>")
                    )
                    sent = True

                if not sent:
                    csock.sendall(
                        _generate_404_output("<html><body>Not Found</body></html>")
                    )

            finally:
                csock.close()

    def get_info(self):
        """
        gets a list of type engine.Items which are statistics of all request from starting webserver
        :return:
        """
        return self.info





