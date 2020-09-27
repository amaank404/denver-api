__version__ = "2020.6.4"

import copy

BASE_FORMAT_KEYS = [
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "bold",
    "italic",
    "heading",
    "sub-heading",
    "title",
    "underlined",
    "block",
    "center",
    "list",
    "url",
    "listitem",
    "str",
    "doc_format"
]
HTML_COMPILE_FORMAT = {
    "h1": "<h1>{text}</h2>",
    "h2": "<h2>{text}</h2>",
    "h3": "<h3>{text}</h3>",
    "h4": "<h4>{text}</h4>",
    "h5": "<h5>{text}</h5>",
    "h6": "<h6>{text}</h6>",
    "bold": "<b>{text}</b>",
    "italic": "<i>{text}</b>",
    "heading": "<h2>{text}</h2>",
    "sub-heading": "<h3>{text}</h3>",
    "title": "<h1>{text}</h1>",
    "underlined": "<u>{text}</u>",
    "block": "<p>{text}</p>",
    "center": "<centre>{text}</centre>",
    "list": "<ul type = \"disk\">{text}</ul>",
    "url": "<a href = \"{url}\">{text}</a>",
    "listitem": "<li>{text}</li>",
    "str": '{text}',
    "doc": """
<!doctype html>
<html>
<head>
<title>
{title}
</title>
<meta charset="utf-8"/>
</head>
<body bgcolor="{backgroundc}" text="{textc}" link="{urlc}">
{text}
<p align="right">
<font color=#aaaaaa size=3>
Made with HandyDocs.
</font>
</p>
</body>
</html>
"""
}
HTML_SYNTAX = {
    "\n": "<br/>",
    "<": "&lt;",
    " ": "&nbsp;",
    ">": "&gt;",
    "\r": ""
}

HTML = (HTML_COMPILE_FORMAT, HTML_SYNTAX)


def parse_element(element: dict, compile_table: dict, compile_syntax: dict):
    p = ''
    for x in element['elements']:
        if type(x) == str:
            p += compile_table['str'].format(text=multi_replace(x, compile_syntax))
        if type(x) == dict:
            p += compile_table[x['class']].format(
                text=parse_element(x, compile_table, compile_syntax),
                **x['attr']
            )
    return p


def compile_doc(doc: dict, compile_format:tuple = HTML):
    c_format, syntax = make_compile_format(compile_format)
    return c_format[doc['class']].format(
                text=parse_element(doc, c_format, syntax),
                **doc['attr']
            )


def make_compile_format(compile_format: tuple):
    _format, syntax = compile_format
    _format = copy.deepcopy(_format)
    syntax = copy.deepcopy(syntax)
    for x in BASE_FORMAT_KEYS:
        if x not in _format.keys():
            _format[x] = '{text}'
    return _format, syntax


def multi_replace(string:str, replace_dict: dict):
    s = string
    for k, v in replace_dict.items():
        s.replace(k,v)
    return s


def main():
    mdoc = doc(
        element(
            element("Hello World", type='bold'),
            type='heading'
        )
    )
    f = open("d.html", 'w')
    f.write(compile_doc(mdoc, HTML))
    f.close()


def element(*elems_str, type, **atr):
    return {"class": type,
            "attr": atr,
            "elements": elems_str}


def doc(*elem, backgroundc='white', title='Unknown', textc="black", urlc='blue', **kwargs):
    kwargs.update(backgroundc=backgroundc, title=title, textc=textc, urlc=urlc)
    return element(*elem, type="doc", **kwargs)


if __name__ == '__main__':
    main()
