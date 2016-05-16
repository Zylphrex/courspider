import re

from html import unescape
from urllib import request


_comments = re.compile('<!--[if.*?]>.*?<![endif]-->')

def get_html(url):
    """
    Retrive the unescaped html string at the give url

    :param url: The url where the html resides
    :type url: str
    :return: The raw html string
    :rtype: str
    """
    with request.urlopen(url) as response:
        html = response.read()

    # decode and unescape the raw html
    # the unescape function turns &nbsp; to some different
    # white space characters, so replace with usual ones
    return _comments.sub("", unescape(html.decode('utf8')).replace(' ', ' '))
