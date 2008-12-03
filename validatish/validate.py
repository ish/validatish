import re, sys
from sets import Set

# Flatten function from http://mail.python.org/pipermail/python-list/2003-October/232886.html
def flatten(s, toiter=iter):
    try:
        it = toiter(s)
    except TypeError:
        yield s
    else:
        for elem in it:
            for subelem in flatten(elem, toiter):
                yield subelem

def keepstrings(seq):
    if isinstance(seq, basestring):
        raise TypeError
    return iter(seq)



class Invalid(Exception):

    def __init__(self, msg, exceptions=None):
        self.msg = msg
        self.exceptions = exceptions

    @property
    def errors(self):
        return list(flatten(self._fetch_errors(),keepstrings))

    def _fetch_errors(self):
        if self.exceptions is None:
            yield self.msg
        else:
            for e in self.exceptions:
                yield e._fetch_errors()



class Validator(object):
    """ Abstract Base class for all validators """

    def __call__(self, value):
        """ A method that will raise an Invalid error """


class CompoundValidator(Validator):
    """ Abstract Base class for compound validators """


##
# STRING

def string(v):
    if v is None:
        return
    msg = "must be a string"
    if not isinstance(v,basestring):
        raise Invalid(msg)

class String(Validator):
    """ Checks whether value can be converted to an integer  """

    def __call__(self, v):
        string(v)


##
# PLAIN TEXT

def plaintext(v,extra=''):
    if v is None:
        return
    if not extra:
        extra.replace('-','\-')
    regex = r"^[a-zA-Z0-9%s]*$"%extra

    msg = "must be a string"
    if not isinstance(v,basestring):
        raise Invalid(msg)

    msg = "must consist of characters and numbers only"
    if extra is not None:
        msg = "must consist of characters and numbers plus any of %s"%extra

    p = re.compile(regex)
    if not p.match(v):
        raise Invalid(msg)

class PlainText(Validator):
    """ Checks whether value is a 'simple' string"""
    def __init__(self, extra=''):
        self.extra = extra
    def __call__(self, v):
        plaintext(v,extra=self.extra)


##
# INTEGER

def integer(v):
    if v is None:
        return
    msg = "must be an integer"
    try:
        if v != int(v):
            raise Invalid(msg)
    except (ValueError, TypeError):
        raise Invalid(msg)
    
class Integer(Validator):
    """ Checks whether value can be converted to an integer  """

    def __call__(self, v):
        integer(v)


##
# NUMBER

def number(v):
    if v is None:
        return
    msg = "must be a number"
    try:
        if isinstance(v,basestring):
            raise Invalid(msg)
        float(v)
    except (ValueError, TypeError):
        raise Invalid(msg)

class Number(Validator):
    """ Checks whether value can be converted to a number and is not a string  """

    def __call__(self, v):
        number(v)

##
# EMAIL

def email(v):
    if v is None:
        return
    msg = "must be an email"
    if not isinstance(v,basestring):
        raise Invalid(msg)
    usernameRE = re.compile(r"^[^ \t\n\r@<>()]+$", re.I)
    addressRE = re.compile(r"^[a-z0-9][a-z0-9\.\-_]*\.[a-z]+$", re.I)
    parts = v.split('@')
    if len(parts) !=2:
        raise Invalid('must have only one @')
    username, address = parts
    if not usernameRE.search(username):
        raise Invalid('username part before the @ is incorrect')
    if not addressRE.search(address):
        raise Invalid('address part after the @ is incorrect')

class Email(Validator):
    """ Checks whether value can be converted to a number and is not a string  """

    def __call__(self, v):
        email(v)

##
# URL

def url(v,with_scheme=False):
    if v is None:
        return
    msg = "must be a url"
    if not isinstance(v,basestring):
        raise Invalid(msg)

    urlRE = re.compile(r'^(http|https)://'
           r'(?:[a-z0-9\-]+|[a-z0-9][a-z0-9\-\.\_]*\.[a-z]+)'
           r'(?::[0-9]+)?'
           r'(?:/.*)?$', re.I) 
    schemeRE = re.compile(r'^[a-zA-Z]+:')
    # Check the scheme matches
    if not with_scheme:
        if not schemeRE.search(v):
            # If we don't have a sceme, add one
            v = 'http://' + v
    # Now get the scheme part back out
    match = schemeRE.search(v)
    if match is None:
        raise Invalid(msg)
    # and use it to help extract the domain part
    v = match.group(0).lower() + v[len(match.group(0)):]
    if not urlRE.search(v):
        raise Invalid(msg)
                             


class URL(Validator):
    """ Checks whether value is a url"""
    def __init__(self, with_scheme=False):
        self.with_scheme = with_scheme

    def __call__(self, v):
        url(v, with_scheme=self.with_scheme)


##
# ONE OF

def oneof(v,set_of_values):
    if v is None:
        return
    if not set_of_values:
        raise Invalid("must be one of []")
    if isinstance(v,list):
        v = tuple(v)

    if v not in Set(set_of_values):
        raise Invalid("must be one of %s"%set_of_values)
    

class OneOf(Validator):
    """ Checks whether value is one of a supplied list of values"""
    def __init__(self, set_of_values):
        self.set_of_values = set_of_values

    def __call__(self, v):
        oneof(v, self.set_of_values)


##
# REQUIRED

def required(v):
    if not v and v != 0:
        raise Invalid("is required")

class Required(Validator):
    """ Checks that the value is not empty
    """

    def __call__(self, v):
        required(v)


##
# LENGTH

def length(v, min=None, max=None):
    if v is None:
        return
    if min is None and max is None:
        return
    if isinstance(v,basestring):
        error = "must have %s than %s characters"
    else:
        error = "must have %s than %s items"
    if max is not None and len(v) > max:
        raise Invalid(error%("less",max))
    if min is not None and len(v) < min:
        raise Invalid(error%("more",min))

class Length(Validator):

    def __init__(self, min=None, max=None):
        self.max = max
        self.min = min

    def __call__(self, v):
        length(v, min=self.min, max=self.max)

##
# RANGE

def range(v, min=None, max=None):
    if min is None and max is None:
        return
    if min is not None and max is not None:
        error = "must be between %s and %s"%(min,max)
    elif min is not None:
        error = "must be greater than %s"%(min)
    else:
        error = "must be less than %s"%(min)
        
    if max is not None and v > max:
        raise Invalid(error)
    if min is not None and v < min:
        raise Invalid(error)

class Range(Validator):

    def __init__(self, min=None, max=None):
        self.max = max
        self.min = min

    def __call__(self, v):
        range(v, min=self.min, max=self.max)


##
# ANY

class Any(CompoundValidator):

    def __init__(self, *args):
        self.validators=args

    def __call__(self, v):
        exceptions = []
        for validator in self.validators:
            try:
                validator(v)
            except Invalid, e :
                exceptions.append(e)
            else:
                return
        raise Invalid("is not valid", exceptions)


##
# ALL

class All(CompoundValidator):

    def __init__(self, *args):
        self.validators = args

    def __call__(self, v):
        exceptions = []
        for validator in self.validators:
            try:
                validator(v)
            except Invalid, e:
                exceptions.append(e)

        if len(exceptions):
            raise Invalid("is not valid", exceptions)


##
# Always

class Always(Validator):
    """
    A validator that always passes, mostly useful as a default.

    This validator tests False to make it seem "invisible" to discourage anyone
    bothering actually calling it.
    """

    def __call__(self, v):
        pass

    def __nonzero__(self):
        return False
        
