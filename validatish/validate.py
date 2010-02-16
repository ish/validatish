"""
Library of basic validation functions.
"""

import re

from validatish.error import Invalid


# Various compiled regexs used in validation functions.
_domain_name_regex = re.compile(r"^[a-z0-9][a-z0-9\.\-_]*\.[a-z]+$", re.I)
_domain_user_regex = re.compile(r"^[^ \t\n\r@<>()]+$", re.I)


def is_required(v,messages=None, none_zero=True):
    """ Checks the non_zero attribute but allows numberic zero to pass """
    # XXX I still think it would be nicer if this just tested "is None". We did
    # discuss about the empty string "", but that's more of an input problem I
    # think, e.g. how does a higher layer interpret something that has not been
    # entered.
    _messages = {
        'required': "is required",
    }
    if messages:
        _messages.update(messages)

    if none_zero:
        if not v and v != 0:
            raise Invalid(_messages['required'])
    else:
        if v is None:
            raise Invalid(_messages['required'])


def is_string(v, messages=None):
    """ checks that the value is an instance of basestring """
    if v is None:
        return
    _messages = {
        'type-string': "must be a string",
    }
    if messages:
        _messages.update(messages)
    if not isinstance(v,basestring):
        raise Invalid(_messages['type-string'])


def is_plaintext(v,extra=None, messages=None):
    """
    Checks that the value contains only alpha-numberics

    :arg extra: A list of extra characters that are allowed
    """
    if v is None:
        return
    if extra:
        extra.replace('-','\-')
    regex = r"^[a-zA-Z0-9%s]*$"%extra

    _messages = {
        'type-string': "must be a string",
        'characters-and-numbers': "must consist of characters and numbers only",
        'characters-and-numbers-extra': "must consist of characters and numbers plus any of %(extra)s",
    }
    if messages:
        _messages.update(messages)

    if not isinstance(v,basestring):
        raise Invalid(_messages['type-string'])

    msg = _messages['characters-and-numbers']
    if extra is not None:
        msg = _messages['characters-and-numbers-extra']%{'extra':extra}

    p = re.compile(regex, re.UNICODE)
    if not p.match(v):
        raise Invalid(msg)


def is_integer(v, messages=None):
    """ Checks that the value can be converted into an integer """
    if v is None:
        return
    _messages = {
        'type-integer': "must be a integer",
    }
    if messages:
        _messages.update(messages)
    try:
        if v != int(v):
            raise Invalid(_messages['type-integer'])
    except (ValueError, TypeError):
        raise Invalid(_messages['type-integer'])


def is_number(v, messages=None):
    """ Checks that the value is not a string but can be converted to a float """
    if v is None:
        return
    _messages = {
        'type-number': "must be a number",
    }
    if messages:
        _messages.update(messages)
    try:
        if isinstance(v,basestring):
            raise Invalid(_messages['type-number'])
        float(v)
    except (ValueError, TypeError):
        raise Invalid(_messages['type-number'])


def is_email(v, messages=None):
    """
    Validate the value looks like an email address.
    """
    if v is None:
        return
    _messages = {
        'type-string': "must be a string",
        'contain-at': "must contain one @",
        'username-incorrect': "username part before the @ is incorrect",
        'domain-incorrect': "domain name part after the @ is incorrect",
    }
    if messages:
        _messages.update(messages)
    if not isinstance(v ,basestring):
        raise Invalid(_messages['type-string'])
    parts = v.split('@')
    if len(parts) !=2:
        raise Invalid(_messages['contain-at'])
    username, address = parts
    if _domain_user_regex.match(username) is None:
        raise Invalid(_messages['username-incorrect'])
    if _domain_name_regex.match(address) is None:
        raise Invalid(_messages['domain-incorrect'])


def is_domain_name(value, messages=None):
    """
    Validate the value looks like a domain name.
    """
    if value is None:
        return
    _messages = {
        'type-string': "must be a string",
        'invalid': "is invalid",
    }
    if messages:
        _messages.update(messages)
    if not isinstance(value, basestring):
        raise Invalid(_messages['type-string'])
    if _domain_name_regex.match(value) is None:
        raise Invalid(_messages['invalid'])


def is_url(v, with_scheme=False, messages=None):
    """ Uses a simple regex from FormEncode to check for a url """
    if v is None:
        return
    _messages = {
        'type-url': "must be a url",
    }
    if messages:
        _messages.update(messages)
    if not isinstance(v,basestring):
        raise Invalid(_messages['type-url'])

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
        raise Invalid(_messages['type-url'])
    # and use it to help extract the domain part
    v = match.group(0).lower() + v[len(match.group(0)):]
    if not urlRE.search(v):
        raise Invalid(_messages['type-url'])


def is_equal(v, compared_to, messages=None):
    """
    Check the value, v, is equal to the comparison value.

    :arg compared_to: the value to compare to
    """
    _messages = {
        'incorrect': "incorrect",
    }
    if messages:
        _messages.update(messages)
    if v is None or v == compared_to:
        return
    raise Invalid(_messages['incorrect'])


def is_one_of(v, set_of_values, messages=None):
    """
    Check that the value is one of the set of values given

    :arg set_of_values: the set of values to check against
    """
    if v is None:
        return
    _messages = {
        'one-of-empty': "must be one of []",
        'one-of': "must be one of %(values)r",
    }
    if messages:
        _messages.update(messages)
    if not set_of_values:
        raise Invalid(_messages['one-of-empty'])
    # XXX what's the following doing?
    if isinstance(v,list):
        v = tuple(v)
    # XXX Why create a set here?
    if v not in set(set_of_values):
        raise Invalid(_messages['one-of']%{'values':set_of_values})


def has_length(v, min=None, max=None, messages=None):
    """
    Check that the length of the string or sequence is not less than an optional min value and not greater than an optional max value

    :arg max: optional max value
    :arg min: optional min value
    """
    if v is None:
        return
    if min is None and max is None:
        return
    _messages = {
        'between': "must have between %(min)s and %(max)s %(unit)s",
        'fewer-than': "must have %(max)s or fewer %(unit)s",
        'more-than': "must have %(min)s or more %(unit)s",
    }
    if messages:
        _messages.update(messages)
    if isinstance(v,basestring):
        unit = 'characters'
    else:
        unit = 'items'
    if max is not None and min is not None and (len(v) > max or len(v) < min):
        raise Invalid(_messages['between']%{'min':min, 'max':max, 'unit':unit})
    if max is not None and len(v) > max:
        raise Invalid(_messages['fewer-than']%{'max':max, 'unit':unit})
    if min is not None and len(v) < min:
        raise Invalid(_messages['more-than']%{'min':min, 'unit':unit})


def is_in_range(v, min=None, max=None, messages=None):
    """
    Check that the value is not less than an optional min value and not greater than an optional max value

    :arg max: optional max value
    :arg min: optional min value
    """

    if min is None and max is None:
        return
    if min is None and max is None:
        return
    _messages = {
        'between': "must have between %(min)s and %(max)s",
        'greater-than': "must be greater than or equal to %(min)s",
        'less-than': "must be less than or equal to %(max)s",
    }
    if min is not None and max is not None:
        error = _messages['between']%{'min':min,'max':max}
    elif min is not None:
        error = _messages['greater-than']%{'min':min}
    else:
        error = _messages['less-than']%{'max':max}
        
    if max is not None and v > max:
        raise Invalid(error)
    if min is not None and v < min:
        raise Invalid(error)

