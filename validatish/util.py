"""
Module of validatish utils.
"""

from validatish.validator import All, Any

def any(iterable):
    return False in (not x for x in iterable)

def all(iterable):
    return True not in (not x for x in iterable)

def validation_includes(validator, validator_type):
    """
    Test if the validator type exists in the validator graph.
    """
    if validator is None:
        return False
    elif isinstance(validator, validator_type):
        return True
    elif isinstance(validator, All):
        return any(validation_includes(v, validator_type) for v in validator.validators)
    elif isinstance(validator, Any):
        included = any(validation_includes(v, validator_type) for v in validator.validators)
        same_type = all(isinstance(v, validator_type) for v in validator.validators)
        return included and same_type
    return False

