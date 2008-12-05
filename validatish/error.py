"""
Module containing package exception classes.
"""


class Invalid(Exception):

    def __init__(self, message, exceptions=None):
        Exception.__init__(self, message, exceptions)
        self.message = message
        self.exceptions = exceptions

    def __str__(self):
        return self.message
    __unicode__ = __str__

    @property
    def errors(self):
        return list(_flatten(self._fetch_errors(), _keepstrings))

    def _fetch_errors(self):
        if self.exceptions is None:
            yield self.message
        else:
            for e in self.exceptions:
                yield e._fetch_errors()


def _flatten(s, toiter=iter):
    try:
        it = toiter(s)
    except TypeError:
        yield s
    else:
        for elem in it:
            for subelem in _flatten(elem, toiter):
                yield subelem


def _keepstrings(seq):
    if isinstance(seq, basestring):
        raise TypeError
    return iter(seq)

