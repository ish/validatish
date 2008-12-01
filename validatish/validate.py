import re
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

    def validate(self, value):
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

    def validate(self, v):
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
    def validate(self, v):
        plaintext(v,extra=self.extra)


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

    def validate(self, v):
        oneof(v, self.set_of_values)

##
# INTEGER

def integer(v):
    if v is None:
        return
    msg = "must be an integer"
    try:
        if v != int(v):
            raise Invalid(msg)
    except:
        raise Invalid(msg)
    
class Integer(Validator):
    """ Checks whether value can be converted to an integer  """

    def validate(self, v):
        integer(v)


##
# Number

def number(v):
    if v is None:
        return
    msg = "must be a number"
    try:
        if isinstance(v,basestring):
            raise Invalid(msg%v)
        float(v)
    except:
        raise Invalid(msg)

class Number(Validator):
    """ Checks whether value can be converted to a number and is not a string  """

    def validate(self, v):
        number(v)


##
# REQUIRED

def required(v):
    if not v and v != 0:
        raise Invalid("is required")

class Required(Validator):
    """ Checks that the value is not empty
    """

    def validate(self, v):
        required(v)


##
# LENGTH

def length(v, min=None, max=None):
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

    def validate(self, v):
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

    def validate(self, v):
        range(v, min=self.min, max=self.max)


##
# ANY

class Any(CompoundValidator):

    def __init__(self, *args):
        self.validators=args

    def validate(self, v):
        exceptions = []
        for validator in self.validators:
            try:
                validator.validate(v)
            except Invalid, e:
                exceptions.append(e)
        if len(exceptions) == len(self.validators):
            raise Invalid("%s is not valid"%v, exceptions)


##
# ALL

class All(CompoundValidator):

    def __init__(self, *args):
        self.validators = args

    def validate(self, v):
        exceptions = []
        for validator in self.validators:
            try:
                validator.validate(v)
            except Invalid, e:
                exceptions.append(e)
        if len(exceptions):
            raise Invalid("%s is not valid"%v, exceptions)



        
