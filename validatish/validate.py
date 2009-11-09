"""
Library of basic validation functions.
"""

import re

from validatish.error import Invalid


# Various compiled regexs used in validation functions.
_domain_name_regex = re.compile(r"^[a-z0-9][a-z0-9\.\-_]*\.[a-z]+$", re.I)
_domain_user_regex = re.compile(r"^[^ \t\n\r@<>()]+$", re.I)


def is_required(v):
    """ Checks the non_zero attribute but allows numberic zero to pass """
    # XXX I still think it would be nicer if this just tested "is None". We did
    # discuss about the empty string "", but that's more of an input problem I
    # think, e.g. how does a higher layer interpret something that has not been
    # entered.
    if not v and v != 0:
        raise Invalid("is required")


def is_string(v):
    """ checks that the value is an instance of basestring """
    if v is None:
        return
    msg = "must be a string"
    if not isinstance(v,basestring):
        raise Invalid(msg)


def is_plaintext(v,extra=None):
    """
    Checks that the value contains only alpha-numberics

    :arg extra: A list of extra characters that are allowed
    """
    if v is None:
        return
    if extra:
        extra.replace('-','\-')
    regex = r"^[a-zA-Z0-9%s]*$"%extra

    msg = "must be a string"
    if not isinstance(v,basestring):
        raise Invalid(msg)

    msg = "must consist of characters and numbers only"
    if extra is not None:
        msg = "must consist of characters and numbers plus any of %s"%extra

    p = re.compile(regex, re.UNICODE)
    if not p.match(v):
        raise Invalid(msg)


def is_integer(v):
    """ Checks that the value can be converted into an integer """
    if v is None:
        return
    msg = "must be an integer"
    try:
        if v != int(v):
            raise Invalid(msg)
    except (ValueError, TypeError):
        raise Invalid(msg)


def is_number(v):
    """ Checks that the value is not a string but can be converted to a float """
    if v is None:
        return
    msg = "must be a number"
    try:
        if isinstance(v,basestring):
            raise Invalid(msg)
        float(v)
    except (ValueError, TypeError):
        raise Invalid(msg)


def is_email(v):
    """
    Validate the value looks like an email address.
    """
    if v is None:
        return
    if not isinstance(v ,basestring):
        raise Invalid("must be a string")
    parts = v.split('@')
    if len(parts) !=2:
        raise Invalid('must contain one @')
    username, address = parts
    if _domain_user_regex.match(username) is None:
        raise Invalid('username part before the @ is incorrect')
    if _domain_name_regex.match(address) is None:
        raise Invalid('domain name part after the @ is incorrect')


def is_domain_name(value):
    """
    Validate the value looks like a domain name.
    """
    if value is None:
        return
    if not isinstance(value, basestring):
        raise Invalid('must be a string')
    if _domain_name_regex.match(value) is None:
        raise Invalid('is invalid')


def is_url(v,with_scheme=False):
    """ Uses a simple regex from FormEncode to check for a url """
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


def is_equal(v, compared_to):
    """
    Check the value, v, is equal to the comparison value.

    :arg compared_to: the value to compare to
    """
    if v is None or v == compared_to:
        return
    raise Invalid("incorrect")


def is_one_of(v, set_of_values):
    """
    Check that the value is one of the set of values given

    :arg set_of_values: the set of values to check against
    """
    if v is None:
        return
    if not set_of_values:
        raise Invalid("must be one of []")
    # XXX what's the following doing?
    if isinstance(v,list):
        v = tuple(v)
    # XXX Why create a set here?
    if v not in set(set_of_values):
        raise Invalid("must be one of %r"%set_of_values)


def has_length(v, min=None, max=None):
    """
    Check that the length of the string or sequence is not less than an optional min value and not greater than an optional max value

    :arg max: optional max value
    :arg min: optional min value
    """
    if v is None:
        return
    if min is None and max is None:
        return
    if isinstance(v,basestring):
        unit = 'characters'
    else:
        unit = 'items'
    if max is not None and min is not None and (len(v) > max or len(v) < min):
        raise Invalid('must have between %s and %s %s'%(min, max, unit))
    if max is not None and len(v) > max:
        raise Invalid('must have %s or fewer %s'%(max, unit))
    if min is not None and len(v) < min:
        raise Invalid('must have %s or more %s'%(min, unit))


def is_in_range(v, min=None, max=None):
    """
    Check that the value is not less than an optional min value and not greater than an optional max value

    :arg max: optional max value
    :arg min: optional min value
    """

    if min is None and max is None:
        return
    if min is not None and max is not None:
        error = "must be between %s and %s"%(min,max)
    elif min is not None:
        error = "must be greater than or equal to %s"%(min)
    else:
        error = "must be less than or equal to %s"%(max)
        
    if max is not None and v > max:
        raise Invalid(error)
    if min is not None and v < min:
        raise Invalid(error)

