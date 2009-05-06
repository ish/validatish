"""
Module containing package exception classes.
"""


class Invalid(Exception):

    def __init__(self, message, exceptions=None, validator=None):
        Exception.__init__(self, message, exceptions)
        self.message = message
        self.exceptions = exceptions
        self.validator = validator

    def __str__(self):
        return self.message
    __unicode__ = __str__

    def __repr__(self):
        if self.exceptions:
            return 'validatish.Invalid("%s", exceptions=%s, validator=%s)' % (self.message, self.exceptions, self.validator)
        else:
            return 'validatish.Invalid("%s", validator=%s)' % (self.message, self.validator)

    @property
    def errors(self):
        return list(_flatten(self._fetch_errors(), _keepstrings))

    def _fetch_errors(self):
        if self.exceptions is None:
            yield self.message
        else:
            for e in self.exceptions:
                yield e._fetch_errors()

    # Hide Python 2.6 deprecation warning.
    def _get_message(self): return self._message
    def _set_message(self, message): self._message = message
    message = property(_get_message, _set_message)


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

