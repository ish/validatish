"""
Library of basic validation functions.
"""

import re

from validatish.error import Invalid


def is_required(v):
    # XXX I still think it would be nicer if this just tested "is None". We did
    # discuss about the empty string "", but that's more of an input problem I
    # think, e.g. how does a higher layer interpret something that has not been
    # entered.
    if not v and v != 0:
        raise Invalid("is required")


def is_string(v):
    if v is None:
        return
    msg = "must be a string"
    if not isinstance(v,basestring):
        raise Invalid(msg)


def is_plaintext(v,extra=''):
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


def is_integer(v):
    if v is None:
        return
    msg = "must be an integer"
    try:
        if v != int(v):
            raise Invalid(msg)
    except (ValueError, TypeError):
        raise Invalid(msg)


def is_number(v):
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


def is_url(v,with_scheme=False):
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
    """
    if v is None or v == compared_to:
        return
    raise Invalid("incorrect")


def is_one_of(v, set_of_values):
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


def is_in_range(v, min=None, max=None):
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

