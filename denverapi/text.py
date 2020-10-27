"""
This Text util is useful in joining two paragraphs so the newlines
don't trouble.
"""
__version__ = "2020.6.4"
__author__ = "Xcodz"

import textwrap


class text:
    def wrap(p, w=70):
        d = [textwrap.fill(x, w) for x in p.split("\n")]
        r = []
        for x in d:
            r.extend(x.split("\n"))
        return r

    def join(p1, p2, *p, w=40, j=""):
        s1 = text.wrap(p1, w - 1)
        s2 = text.wrap(p2, w - 1)
        s = [text.wrap(x, w - 1) for x in p]
        s.insert(0, s2.copy())
        del s2
        lenl = max(*([len(s[x]) for x in range(len(s))] + [len(s1)]))
        text.vfill(s1, lenl)
        for x in range(len(s)):
            for y in range(len(s[x])):
                s[x][y] = text.linefill(s[x][y], w)
        for y in range(len(s1)):
            s1[y] = text.linefill(s1[y], w)
        for x in s:
            text.vfill(x, lenl)
        for x in range(len(s)):
            for y in range(len(s[x])):
                s1[y] += j + s[x][y]
        return "\n".join(s1)

    def linefill(l, width, fill=" "):
        return l + (fill * (width - len(l)))

    def vfill(l, length, fill=""):
        l.extend([fill for _ in range(length - len(l))])
