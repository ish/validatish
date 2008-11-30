class Invalid(Exception):

    def __init__(self, msg, errors=None):
        self.msg = msg
        self.errors = errors

    def __str__(self):
        return self.msg

    def __repr__(self):
        error_msg = '\n'.join(self.list_errors())
        return '%s\n---------\n%s'%(self.msg, error_msg)

    def list_errors(self):
        if self.errors is None:
            yield self.msg
        else:
            for e in self.errors:
                e.list_errors()





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
    if not isinstance(v,basestring):
        raise Invalid("%s is not a string"%v)

class String(Validator):
    """ Checks whether value can be converted to an integer  """

    def validate(self, v):
        string(v)


##
# INTEGER

def integer(v):
    try:
        if v != int(v):
            raise
    except:
        raise Invalid("%s is not an integer"%v)
    
class Integer(Validator):
    """ Checks whether value can be converted to an integer  """

    def validate(self, v):
        integer(v)


##
# REQUIRED

def nonzero(v):
    if not v:
        raise Invalid("%s is required"%v)

class Required(Validator):
    """ Checks that the value is not empty
    """

    def validate(self, v):
        nonezero(v)


##
# LENGTH

def check_length(v, min=None, max=None):
    if isinstance(v,basestring):
        error = "%s cannot have %s than %s characters"
    else:
        error = "%s cannot have %s than %s items"
    if max is not None and len(v) > max:
        raise Invalid(error%(v,"more",max))
    if min is not None and len(v) < min:
        raise Invalid(error%(v,"less",min))

class Length(Validator):

    def __init__(self, min=None, max=None):
        self.max = max
        self.min = min

    def validate(self, v):
        check_length(v, min=self.min, max=self.max)

##
# ANY

class Any(CompoundValidator):

    def __init__(self, *args):
        self.validators=args

    def validate(self, v):
        errors = []
        for validator in self.validators:
            try:
                validator.validate(v)
            except Invalid, e:
                errors.append(e)
        if len(errors) == len(self.validators):
            raise Invalid("%s is not valid"%v, errors)


##
# ALL

class All(CompoundValidator):

    def __init__(self, *args):
        self.validators = args

    def validate(self, v):
        errors = []
        for validator in self.validators:
            try:
                validator.validate(v)
            except Invalid, e:
                errors.append(e)
        if len(errors):
            raise Invalid("%s is not valid"%v, errors)



        
