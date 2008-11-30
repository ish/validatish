import unittest
from validatish import validate


def error_message(type,self,v,e):
    if type == 'function':
        return "'%s' secton of function '%s' on '%s' failed with %s"%(
            self.section, self.type, v, e.msg)
    if type == 'class':
        return "'%s' secton of object '%s' on '%s' failed with %s"%(
            self.section, self.type.lower(), v, e.msg)

def check_pass(type, self, fn, values):
    for v in values:
        try:
            # Attempt validation using function
            fn(v)
        except Exception, e:
            self.fail(error_message(type,self,v,e))

def check_fail(type, self, fn, values):
    for v in values:
        try:
            fn(v)
        except validate.Invalid, e:
            continue
        except Exception, e:
            self.fail(error_message(type,self,v,e))

class TestString(unittest.TestCase):

    type='String'

    def test_validate_pass(self):
        self.section='pass'
        values = [
            'foo',
            '1',
            u'foobar',
            'sad',
            None,
            ]
        fn = validate.string
        check_pass('function',self, fn, values)
        fn = validate.String().validate
        check_pass('class', self, fn, values)

    def test_validate_fail(self):
        self.section='pass'
        values = [
            1,
            1.01,
            ['a','b','c'],
            ['a'],
            ]
        fn = validate.string
        check_fail('function', self, fn, values)
        validator = validate.String().validate
        check_fail('class', self, fn, values)


class TestInteger(unittest.TestCase):

    type='Integer'

    def test_validate_pass(self):
        self.section='pass'
        values = [
            1,
            -1,
            0,
            1.0,
            1L,
            ]
        fn = validate.integer
        check_pass('function',self, fn, values)
        fn = validate.Integer().validate
        check_pass('class', self, fn, values)

    def test_validate_fail(self):
        self.section='pass'
        values = [
            1.01,
            'foo',
            ['a','b','c'],
            '1',
            ]
        fn = validate.integer
        check_fail('function', self, fn, values)
        validator = validate.Integer().validate
        check_fail('class', self, fn, values)


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
        fn = validate.required
        check_pass('function',self, fn, values)
        fn = validate.Required().validate
        check_pass('class', self, fn, values)

    def test_validate_fail(self):
        values = [
            '',
            [],
            u'',
            ]
        fn = validate.required
        check_fail('function', self, fn, values)
        validator = validate.Required().validate
        check_fail('class', self, fn, values)
