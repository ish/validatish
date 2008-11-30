
import unittest
from validatish import validate

from datetime import datetime


class TestAll(unittest.TestCase):

    def test_validate_pass(self):
        values = [
            '1',
            '4',
            u'3'
        ]
        validator = validate.All(validate.String(), validate.Required())
        for v in values:
            validator.validate(v)


    def test_validate_fail(self):
        values = [
            '',
            u'',
            0,
        ]
        validator = validate.All(validate.String(), validate.Required())
        for v in values:
            self.assertRaises(validate.Invalid,validator.validate, v)


class TestAny(unittest.TestCase):

    def test_validate_pass(self):
        values = [
            '1',
            4,
            1L,
            None,
        ]
        validator = validate.Any(validate.String(), validate.Integer())
        for v in values:
            print 'checking %s'%v
            validator.validate(v)


    def test_validate_fail(self):
        values = [
            0.5,
            datetime.now(),
        ]
        validator = validate.Any(validate.String(), validate.Integer())
        for v in values:
            print 'checking %s'%v
            self.assertRaises(validate.Invalid,validator.validate, v)
