__author__ = 'soroosh'
from datetime import datetime


class Action:
    def regex(self): raise NotImplementedError()

    def response(self, *args, **kwargs): raise NotImplementedError()


class HelloWorldAction(Action):
    def regex(self): return 'GET /\sHTTP/1'

    def response(self, *args, **kwargs):
        return """<html><body>Hello World</body></html>
        """

    def mime_type(self): return 'text/html'


class PicAction(Action):
    def regex(self): return 'GET /pic\sHTTP/1'

    def response(self, *args, **kwargs):
        with open('img.jpg', 'r') as f:
            img_data = f.read()
            return img_data

    def mime_type(self): return 'image/jpeg'


class ClientAction(Action):
    def __init__(self, get_info_callback):
        self._get_info_callback = get_info_callback

    def regex(self): return 'GET /clients.html\sHTTP/1'

    def mime_type(self): return 'text/html'

    def response(self, *args, **kwargs):
        result = self._get_info_callback()
        template = '<html><body>%s</body</html>'
        table = '<table border=1><tr><td>Client Address</td><td>Headers</td><td>Client Opened Port</td></tr> %s</table>'
        rows = ''
        for item in result:
            rows = rows + '<tr><td>%s</td><td>%s</td><td>%s</td><tr>' % (item.ip, item.headers, item.opened_port)

        return template % (table % rows)


class TimeAction(Action):
    def regex(self): return 'GET /time.php\sHTTP/1'

    def mime_type(self): return 'text/html'

    def response(self, *args, **kwargs):
        return '<html><body>Time on %s</body></html>' % (kwargs['host'] + ' is ' + str(datetime.now()))


class DirAction(Action):
    def regex(self):
        return 'GET /server/(.*)\sHTTP/1'

    def mime_type(self):
        return 'text/html'

    def response(self, *args, **kwargs):
        print kwargs['params']
        try:
            with open(kwargs['params'][0], 'r') as f:
                return '<html><body>%s</body></html>' % (f.read().replace('\r\n', '<br />').replace('\n', '<br />'))
        except Exception as e:
            return '<html><body>File does not exist</body></html>'


