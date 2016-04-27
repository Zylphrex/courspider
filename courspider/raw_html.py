import urllib.request


def get_html(url):
    """
    Retrive the raw html string at the give url

    :param url: The url where the html resides
    :type url: str
    :return: The raw html string
    :rtype: str
    """
    with urllib.request.urlopen(url) as response:
        html = response.read()
    return html.decode('utf8')
