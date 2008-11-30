import unittest
from validatish import validate


class TestString(unittest.TestCase):

    def test_validate_pass(self):
        values = [
            'foo',
            '1',
            u'foobar',
            'sad',
            None,
            ]
        for v in values:
            print 'checking %s'%v
            validate.string(v)
        validator = validate.String()
        for v in values:
            print 'checking %s'%v
            validator.validate(v)


    def test_validate_fail(self):
        values = [
            1,
            1.01,
            ['a','b','c'],
            ['a'],
            ]
        for v in values:
            print 'checking %s'%v
            self.assertRaises(validate.Invalid,validate.string, v)
        validator = validate.String()
        for v in values:
            print 'checking %s'%v
            self.assertRaises(validate.Invalid,validator.validate, v)


class TestInteger(unittest.TestCase):

    def test_validate_pass(self):
        values = [
            1,
            -1,
            0,
            1.0,
            1L,
            None,
            ]
        for v in values:
            print 'checking %s'%v
            validate.integer(v)
        validator = validate.Integer()
        for v in values:
            print 'checking %s'%v
            validator.validate(v)

    def test_validate_fail(self):
        values = [
            1.01,
            'foo',
            ['a','b','c'],
            '1',
            ]
        for v in values:
            print 'checking %s'%v
            self.assertRaises(validate.Invalid,validate.integer, v)
        validator = validate.Integer()
        for v in values:
            print 'checking %s'%v
            self.assertRaises(validate.Invalid,validator.validate, v)


class TestRequired(unittest.TestCase):

    def test_validate_pass(self):
        values = [
            0.0,
            ' ',
            [''],
            '0',
            [None],
            'None',
            ]
        for v in values:
            print 'checking %s'%v
            validate.required(v)
        validator = validate.Required()
        for v in values:
            print 'checking %s'%v
            validator.validate(v)

    def test_validate_fail(self):
        values = [
            '',
            [],
            u'',
            ]
        for v in values:
            print 'checking %s'%v
            self.assertRaises(validate.Invalid,validate.required, v)
        validator = validate.Required()
        for v in values:
            print 'checking %s'%v
            self.assertRaises(validate.Invalid,validator.validate, v)

