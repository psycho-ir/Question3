import re
import socket
from actions import HelloWorldAction, PicAction, ClientAction, TimeAction, DirAction, MyAction

__author__ = 'soroosh'
import logging

logging.basicConfig(level=logging.INFO)


class Info:
    def __init__(self, ip, headers, opened_port):
        self.opened_port = opened_port
        self.headers = headers
        self.ip = ip


class WebServer:
    def __init__(self, port, host=''):
        self.host = host
        self.port = port
        self.paused = False
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.actions = []
        self.info = []

    def register_action(self, action):
        self.actions.append(action)

    def start(self):
        self._socket.bind((self.host, self.port))
        self._socket.listen(100)
        self._run_event_loop()

    def _run_event_loop(self):
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
                        m = re.match(r'.*\r\nHost: (.*)\r\n', req, re.MULTILINE)
                        if not m:
                            params =[]
                            host = ''
                        else:
                            params = match.groups()
                            host =m.group(1)

                        csock.sendall(self._generate_output(action.response(request=req, ip=caddr[0], port=caddr[1], params=params, host=host), action.mime_type()))
                        sent = True
                        break
                if not re.match('^GET.*',req):
                    csock.sendall(
                        self._generate_500_output("<html><body>Method Not Allowed</body></html>")
                    )
                    sent = True

                if not sent:
                    csock.sendall(
                        self._generate_404_output("<html><body>Not Found</body></html>")
                    )

            finally:
                csock.close()

    def get_info(self):
        return self.info

    def _generate_output(self, content, mimetype='text/html'):
        return """HTTP/1.1 200 OK
Content - Type: %s

%s""" % (mimetype, content)

    def _generate_404_output(self, content):
        return """HTTP/1.1 404 NOT FOUND
Content - Type: %s

%s""" % ('text/html', content)

    def _generate_500_output(self, content):
        return """HTTP/1.1 500 Method Not Allowed
Content - Type: %s

%s""" % ('text/html', content)


s = WebServer(8007)
s.register_action(HelloWorldAction())
s.register_action(PicAction())
s.register_action(ClientAction(s.get_info))
s.register_action(TimeAction())
s.register_action(DirAction())
s.register_action(MyAction())
s.start()



