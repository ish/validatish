from validatish import validate
from error import Invalid


#####
# Validator base classes.
#


class Validator(object):
    """ Abstract Base class for all validators """

    def __call__(self, value):
        """ A method that will raise an Invalid error """

    def __repr__(self):
        return 'validatish.%s()'%self.__class__.__name__


class CompoundValidator(Validator):
    """ Abstract Base class for compound validators """
    validators = None


#####
# Validators types.
#


class Required(Validator):
    """ Checks that the value is not empty
    """

    def __call__(self, v):
        try:
            validate.is_required(v)
        except Invalid, e:
            raise Invalid(e.message, validator=self)



class String(Validator):
    """ Checks whether value can be converted to an integer  """

    def __call__(self, v):
        try:
            validate.is_string(v)
        except Invalid, e:
            raise Invalid(e.message, validator=self)


class PlainText(Validator):
    """ Checks whether value is a 'simple' string"""
    def __init__(self, extra=''):
        self.extra = extra
    def __call__(self, v):
        try:
            validate.is_plaintext(v,extra=self.extra)
        except Invalid, e:
            raise Invalid(e.message, validator=self)


class Email(Validator):
    """ Checks whether value looks like an email address.  """

    def __call__(self, v):
        try:
            validate.is_email(v)
        except Invalid, e:
            raise Invalid(e.message, validator=self)


class DomainName(Validator):
    """ Checks whether value looks like a domain name.  """

    def __call__(self, v):
        try:
            validate.is_domain_name(v)
        except Invalid, e:
            raise Invalid(e.message, validator=self)


class URL(Validator):
    """ Checks whether value is a url"""
    def __init__(self, with_scheme=False):
        self.with_scheme = with_scheme

    def __call__(self, v):
        try:
            validate.is_url(v, with_scheme=self.with_scheme)
        except Invalid, e:
            raise Invalid(e.message, validator=self)

    def __repr__(self):
        return 'validatish.%s(with_schema=%s)'%(self.__class__.__name__, self.with_scheme)


class Integer(Validator):
    """ Checks whether value can be converted to an integer  """

    def __call__(self, v):
        try:
            validate.is_integer(v)
        except Invalid, e:
            raise Invalid(e.message, validator=self)


class Number(Validator):
    """ Checks whether value can be converted to a number and is not a string  """

    def __call__(self, v):
        try:
            validate.is_number(v)
        except Invalid, e:
            raise Invalid(e.message, validator=self)


class Equal(Validator):
    """
    Validator that checks a value is equal to the comparison value, equal_to.
    """
    def __init__(self, compared_to):
        self.compared_to = compared_to

    def __call__(self, v):
        try:
            validate.is_equal(v, self.compared_to)
        except Invalid, e:
            raise Invalid(e.message, validator=self)

    def __repr__(self):
        return 'validatish.%s(%s)'%(self.__class__.__name__, self.compared_to)


class OneOf(Validator):
    """ Checks whether value is one of a supplied list of values"""
    def __init__(self, set_of_values):
        self.set_of_values = set_of_values

    def __call__(self, v):
        try:
            validate.is_one_of(v, self.set_of_values)
        except Invalid, e:
            raise Invalid(e.message, validator=self)

    def __repr__(self):
        return 'validatish.%s(%s)'%(self.__class__.__name__, self.set_of_values)


class Length(Validator):
    """ Check whether the length of the value is not outside min/max bound(s) """

    def __init__(self, min=None, max=None):
        self.max = max
        self.min = min

    def __call__(self, v):
        try:
            validate.has_length(v, min=self.min, max=self.max)
        except Invalid, e:
            raise Invalid(e.message, validator=self)

    def __repr__(self):
        return 'validatish.%s(min=%s, max=%s)'%(self.__class__.__name__, self.min, self.max)


class Range(Validator):
    """ Check whether the value is not outside min/max bound(s) """

    def __init__(self, min=None, max=None):
        self.max = max
        self.min = min

    def __call__(self, v):
        try:
            validate.is_in_range(v, min=self.min, max=self.max)
        except Invalid, e:
            raise Invalid(e.message, validator=self)

    def __repr__(self):
        return 'validatish.%s(min=%s, max=%s)'%(self.__class__.__name__, self.min, self.max)


class Any(CompoundValidator):
    """
    Combines multiple validators together, raising an exception only if they
    all fail (i.e. validation succeeds if any validator passes).
    """

    def __init__(self, *args):
        self.validators=args

    def __call__(self, v):
        exceptions = []
        for validator in self.validators:
            try:
                validator(v)
            except Invalid, e :
                exceptions.append(Invalid(e.message, e.exceptions, validator))
            else:
                return
        message = '; '.join(e.message for e in exceptions)
        raise Invalid("Please fix any of: %s"%message, exceptions, self)

    def __repr__(self):
        return 'validatish.%s%s'%(self.__class__.__name__, self.validators)


class All(CompoundValidator):
    """ Combines multiple validators together, raising an exception unless they all pass """

    def __init__(self, *args):
        self.validators = args

    def __call__(self, v):
        exceptions = []
        for validator in self.validators:
            try:
                validator(v)
            except Invalid, e:
                exceptions.append(Invalid(e.message, e.exceptions, validator))

        if len(exceptions):
            message = '; '.join(e.message for e in exceptions)
            raise Invalid(message, exceptions, self)

    def __repr__(self):
        return 'validatish.%s%s'%(self.__class__.__name__, self.validators)


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

