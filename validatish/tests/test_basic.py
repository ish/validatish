import unittest, sys
from validatish import validate
from datetime import datetime


def error_message(type,self,v,e):
    msg = getattr(e,'msg',repr(e))
    if type == 'function':
        return "'%s' secton of function %s(%s) failed with %s"%(
            self.section, self.type, v, msg)
    if type == 'class':
        return "'%s' secton of object %s(%s)' failed with %s"%(
            self.section, self.type.lower(), v, msg)

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
            self.fail(error_message(type,self,v,'incorrectly passed validation'))
        except validate.Invalid:
            continue
        except AssertionError:
            raise
        except:
            e = sys.exc_info()[1]
            self.fail(error_message(type,self,v,e))


class TestString(unittest.TestCase):

    type='String'
    fn = staticmethod(validate.string)
    class_fn = validate.String().validate

    def test_validate_pass(self):
        self.section='pass'
        values = [
            'foo',
            '1',
            u'foobar',
            'sad',
            None,
            ]
        check_pass('function',self, self.fn, values)
        check_pass('class', self, self.class_fn, values)

    def test_validate_fail(self):
        self.section='pass'
        values = [
            1,
            1.01,
            ['a','b','c'],
            ['a'],
            ]
        check_fail('function', self, self.fn, values)
        check_fail('class', self, self.class_fn, values)


class TestInteger(unittest.TestCase):

    type='Integer'
    fn = staticmethod(validate.integer)
    class_fn = validate.Integer().validate

    def test_validate_pass(self):
        self.section='pass'
        values = [
            1,
            -1,
            0,
            1.0,
            1L,
            ]
        check_pass('function',self, self.fn, values)
        check_pass('class', self, self.class_fn, values)

    def test_validate_fail(self):
        self.section='pass'
        values = [
            1.01,
            'foo',
            ['a','b','c'],
            '1',
            ]
        check_fail('function', self, self.fn, values)
        check_fail('class', self, self.class_fn, values)

class TestNumber(unittest.TestCase):

    type='Number'
    fn = staticmethod(validate.number)
    class_fn = validate.Number().validate

    def test_validate_pass(self):
        self.section='pass'
        values = [
            1,
            -1,
            0,
            1.0,
            1L,
            1.01,
            1E6,
            -3.1415926,
            ]
        check_pass('function',self, self.fn, values)
        check_pass('class', self, self.class_fn, values)

    def test_validate_fail(self):
        self.section='pass'
        values = [
            'foo',
            ['a','b','c'],
            '1',
            ]
        check_fail('function', self, self.fn, values)
        check_fail('class', self, self.class_fn, values)

class TestRequired(unittest.TestCase):

    type='Required'
    fn = staticmethod(validate.required)
    class_fn = validate.Required().validate

    def test_validate_pass(self):
        self.section='pass'
        values = [
            0.0,
            ' ',
            [''],
            '0',
            [None],
            'None',
            ]
        check_pass('function',self, self.fn, values)
        check_pass('class', self, self.class_fn, values)

    def test_validate_fail(self):
        self.section='fail'
        values = [
            '',
            [],
            u'',
            ]
        check_fail('function', self, self.fn, values)
        check_fail('class', self, self.class_fn, values)


class TestLength(unittest.TestCase):

    type = 'Length'

    fn_min = staticmethod( lambda v: validate.length(v, min=3) )
    class_fn_min = validate.Length(min=3).validate

    fn_max = staticmethod( lambda v: validate.length(v, max=3) )
    class_fn_max = validate.Length(max=3).validate

    def test_validate_min_pass(self):
        self.section='pass'
        values = [
            'abc',
            ['a','b','c'],
            ]
        check_pass('function', self, self.fn_min, values)
        check_pass('class', self, self.class_fn_min, values)

    def test_validate_min_fail(self):
        self.section='fail'
        values = [
            'a',
            'ab',
            '',
            [],
            ['a'],
            ['ab'],
            ]
        check_fail('function', self, self.fn_min, values)
        check_fail('class', self, self.class_fn_min, values)

    def test_validate_max_pass(self):
        self.section='pass'
        values = [
            'abc',
            ['a','b','c'],
            '',
            [],
            ['abcd'],
            ]
        check_pass('function', self, self.fn_max, values)
        check_pass('class', self, self.class_fn_max, values)

    def test_validate_max_fail(self):
        self.section='fail'
        values = [
            'abcde',
            'abcd',
            ['a','b','c','d'],
            ]
        check_fail('function', self, self.fn_max, values)
        check_fail('class', self, self.class_fn_max, values)

    def test_messages(self):
        try:
            self.fn_min('')
        except validate.Invalid, e:
            assert 'more' in e.msg
        try:
            self.fn_max('aaaaaaaaaa')
        except validate.Invalid, e:
            assert 'less' in e.msg

class TestRange(unittest.TestCase):

    type = 'Range'

    fn_min = staticmethod( lambda v: validate.range(v, min=3) )
    class_fn_min = validate.Range(min=3).validate

    fn_max = staticmethod( lambda v: validate.range(v, max=3) )
    class_fn_max = validate.Range(max=3).validate

    fn_between = staticmethod( lambda v: validate.range(v, min=1,max=3) )
    class_fn_between = validate.Range(min=1,max=3).validate

    def test_validate_min_pass(self):
        self.section='pass'
        values = [
            4,
            5.5,
            ]
        check_pass('function', self, self.fn_min, values)
        check_pass('class', self, self.class_fn_min, values)

    def test_validate_min_fail(self):
        self.section='fail'
        values = [
            0,
            -1,
            -0.23,
            ]
        check_fail('function', self, self.fn_min, values)
        check_fail('class', self, self.class_fn_min, values)

    def test_validate_max_pass(self):
        self.section='pass'
        values = [
            0,
            -1,
            -0.23,
            2.99,
            ]
        check_pass('function', self, self.fn_max, values)
        check_pass('class', self, self.class_fn_max, values)

    def test_validate_max_fail(self):
        self.section='fail'
        values = [
            4,
            5,
            6.9845,
            ]
        check_fail('function', self, self.fn_max, values)
        check_fail('class', self, self.class_fn_max, values)

    def test_validate_between_pass(self):
        self.section='pass'
        values = [
            1.4,
            1,
            2.23,
            2.99,
            3,
            ]
        check_pass('function', self, self.fn_between, values)
        check_pass('class', self, self.class_fn_between, values)

    def test_validate_between_fail(self):
        self.section='fail'
        values = [
            4,
            5,
            6.9845,
            0,
            -2,
            -9,
            ]
        check_fail('function', self, self.fn_between, values)
        check_fail('class', self, self.class_fn_between, values)

    def test_messages(self):
        try:
            self.fn_min(-999999)
        except validate.Invalid, e:
            assert 'greater' in e.msg
        try:
            self.fn_max(999999)
        except validate.Invalid, e:
            assert 'less' in e.msg
        try:
            self.fn_between(-999999)
        except validate.Invalid, e:
            assert 'between' in e.msg
        

class TestAll_StringRequired(unittest.TestCase):

    type='All'
    fn = validate.All(validate.String(), validate.Required()).validate

    def test_validate_pass(self):
        self.section='pass'
        values = [
            '1',
            '4',
            u'3'
        ]
        check_pass('class', self, self.fn, values)


    def test_validate_fail(self):
        self.section='fail'
        values = [
            '',
            u'',
            0,
        ]
        check_fail('class', self, self.fn, values)


class TestAny_IntegerString(unittest.TestCase):

    type='Any'
    fn = validate.Any(validate.String(), validate.Integer()).validate

    def test_validate_pass(self):
        self.section='pass'
        values = [
            '1',
            1,
            1L,
            None,
            ]
        check_pass('class', self, self.fn, values)

    def test_validate_fail(self):
        self.section='fail'
        values = [
            0.5,
            datetime.now(),
        ]
        check_fail('class', self, self.fn, values)



