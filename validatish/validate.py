

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
        pass

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



        
