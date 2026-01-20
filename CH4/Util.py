
import HTMLParser

def load(url):
    body = url.request()
    HTMLParser(body).parse()