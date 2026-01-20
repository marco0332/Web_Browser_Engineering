import HTMLParser

def load(url):
    body = url.request()
    HTMLParser(body).parse()

def paint_tree(layout_object, display_list):
    display_list.extend(layout_object.paint())

    for child in layout_object.children:
        paint_tree(child, display_list)