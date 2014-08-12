__author__ = 'soroosh'


def _generate_output(content, mimetype='text/html'):
    return """HTTP/1.1 200 OK
Content - Type: %s

%s""" % (mimetype, content)


def _generate_404_output(content):
    return """HTTP/1.1 404 NOT FOUND
Content - Type: %s

%s""" % ('text/html', content)


def _generate_500_output(content):
    return """HTTP/1.1 500 Method Not Allowed
Content - Type: %s

%s""" % ('text/html', content)
