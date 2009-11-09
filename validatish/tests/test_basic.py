import unittest
from validatish import error, validate, validator, util
from datetime import datetime


def error_message(type,self,v,e):
    msg = getattr(e,'msg',repr(e))
    if type == 'function':
        return "'%s' secton of function %s(%s) failed with %s"%(
            self.section, self.type, repr(v), msg)
    if type == 'class':
        return "'%s' secton of object %s(%s)' failed with %s"%(
            self.section, self.type.lower(), repr(v), msg)

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
        except error.Invalid:
            continue
        except AssertionError:
            raise

class TestString(unittest.TestCase):

    type='String'
    fn = staticmethod(validate.is_string)
    class_fn = validator.String()

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
        self.section='fail'
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
    fn = staticmethod(validate.is_integer)
    class_fn = validator.Integer()

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
        self.section='fail'
        values = [
            1.01,
            'foo',
            ['a','b','c'],
            '1',
            ]
        check_fail('function', self, self.fn, values)
        check_fail('class', self, self.class_fn, values)

class TestPlainText(unittest.TestCase):

    type='PlainText'
    fn = staticmethod(validate.is_plaintext)
    class_fn = validator.PlainText()

    fn_extra_underline = staticmethod( lambda v: validate.is_plaintext(v,extra='_') )
    class_fn_extra_underline = validator.PlainText(extra='_')

    fn_extra_hyphen = staticmethod( lambda v: validate.is_plaintext(v,extra='-') )
    class_fn_extra_hyphen = validator.PlainText(extra='-')

    def test_validate_pass(self):
        self.section='pass'
        values = [
            'foo',
            'a99',
            '99a',
            '99',
            '',
            None,
            ]
        check_pass('function',self, self.fn, values)
        check_pass('class', self, self.class_fn, values)

    def test_validate_fail(self):
        self.section='fail'
        values = [
            1,
            1.01,
            ['a','b','c'],
            ['a'],
            'rew_',
            'a-',
            'a f',
            ]
        check_fail('function', self, self.fn, values)
        check_fail('class', self, self.class_fn, values)

    def test_validate_underline_pass(self):
        self.section='pass'
        values = [
            'foo',
            'a99',
            '99a',
            'rew_',
            '99',
            '',
            '_',
            None,
            ]
        check_pass('function',self, self.fn_extra_underline, values)
        check_pass('class', self, self.class_fn_extra_underline, values)

    def test_validate_underline_fail(self):
        self.section='fail'
        values = [
            1,
            1.01,
            ['a','b','c'],
            ['a'],
            'a-',
            'a f',
            ]
        check_fail('function', self, self.fn_extra_underline, values)
        check_fail('class', self, self.class_fn_extra_underline, values)

    def test_validate_hyphen_pass(self):
        self.section='pass'
        values = [
            'foo',
            'a99',
            '99a',
            '99',
            '',
            None,
            'a-',
            '-',
            ]
        check_pass('function',self, self.fn_extra_hyphen, values)
        check_pass('class', self, self.class_fn_extra_hyphen, values)

    def test_validate_hyphen_fail(self):
        self.section='fail'
        values = [
            1,
            1.01,
            ['a','b','c'],
            ['a'],
            'a f',
            'rew_',
            '_',
            ]
        check_fail('function', self, self.fn_extra_hyphen, values)
        check_fail('class', self, self.class_fn_extra_hyphen, values)


class TestEmail(unittest.TestCase):

    type='Email'
    fn = staticmethod(validate.is_email)
    class_fn = validator.Email()

    def test_validate_pass(self):
        self.section='pass'
        values = [
            'r@t.p',
            'info@timparkin.co.uk',
            #'root@192.168.1.1', # Failing at the moment - get a better regexp
            None,
            ]
        check_pass('function',self, self.fn, values)
        check_pass('class', self, self.class_fn, values)

    def test_validate_fail(self):
        self.section='fail'
        values = [
            1,
            1.01,
            ['a','b','c'],
            ['a'],
            '@derek.com',
            'tim@eliot',
            'info@tim@parkin.co.uk',
            ]
        check_fail('function', self, self.fn, values)
        check_fail('class', self, self.class_fn, values)


class TestDomainName(unittest.TestCase):

    type='DomainName'
    fn = staticmethod(validate.is_domain_name)
    class_fn = validator.DomainName()

    def test_validate_pass(self):
        self.section='pass'
        values = [
            't.p',
            'timparkin.co.uk',
            None,
            ]
        check_pass('function',self, self.fn, values)
        check_pass('class', self, self.class_fn, values)

    def test_validate_fail(self):
        self.section='fail'
        values = [
            1,
            1.01,
            ['a','b','c'],
            ['a'],
            'derekcom',
            'tim@eliot',
            'info@tim@parkin.co.uk',
            ]
        check_fail('function', self, self.fn, values)
        check_fail('class', self, self.class_fn, values)


class TestURL(unittest.TestCase):

    type='URL'
    fn = staticmethod(validate.is_url)
    class_fn = validator.URL()

    def test_validate_pass(self):
        self.section='pass'
        values = [
            'foo.com',
            #'192,168.1.1',#Fails at the moment
            None,
            ]
        check_pass('function',self, self.fn, values)
        check_pass('class', self, self.class_fn, values)

    def test_validate_fail(self):
        self.section='fail'
        values = [
            1,
            1.01,
            ['a','b','c'],
            ['a'],
            '@derek.com',
            'tim@eliot',
            'htt-p://google.com',
            ]
        check_fail('function', self, self.fn, values)
        check_fail('class', self, self.class_fn, values)

    def test_validate_pass_withoutscheme(self):
        fn = lambda v: validate.is_url(v, with_scheme=True)
        self.section='pass'
        values = [
            'http://foo.com',
            ]
        check_pass('function', self, fn, values)


    def test_validate_withoutscheme(self):
        fn = lambda v: validate.is_url(v, with_scheme=True)
        self.section='fail'
        values = [
            'foo.com',
            ]
        check_fail('function', self, fn, values)


class TestNumber(unittest.TestCase):

    type='Number'
    fn = staticmethod(validate.is_number)
    class_fn = validator.Number()

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
            None,
            ]
        check_pass('function',self, self.fn, values)
        check_pass('class', self, self.class_fn, values)

    def test_validate_fail(self):
        self.section='fail'
        values = [
            'foo',
            ['a','b','c'],
            '1',
            ]
        check_fail('function', self, self.fn, values)
        check_fail('class', self, self.class_fn, values)

class TestRequired(unittest.TestCase):

    type='Required'
    fn = staticmethod(validate.is_required)
    class_fn = validator.Required()

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


class TestEquals(unittest.TestCase):

    type = 'Equals'
    fn = staticmethod(lambda v: validate.is_equal(v, 'matches this'))
    class_fn = validator.Equal('matches this')

    def test_validate_pass(self):
        self.section='pass'
        values = ['matches this']
        check_pass('function',self, self.fn, values)
        check_pass('class', self, self.class_fn, values)

    def test_validate_fail(self):
        self.section='fail'
        values = [
            'foo',
            ['a','b','c'],
            '1',
            2,
            4,
            6,
            8,
            10,
            '',
            [],
            ]
        check_fail('function', self, self.fn, values)
        check_fail('class', self, self.class_fn, values)


class TestOneOf(unittest.TestCase):

    type='OneOf'
    fn = staticmethod( lambda v: staticmethod(validate.is_one_of(v,[3,5,7,9])))
    class_fn = validator.OneOf([3,5,7,9])

    fn_chars = staticmethod( lambda v: staticmethod(validate.is_one_of(v,'ynsbl')))
    class_fn_chars = validator.OneOf('ynsbl')

    fn_list_tuples = staticmethod( lambda v: staticmethod(validate.is_one_of(v,[(1,2),(3,4),(5,6)])))
    class_fn_list_tuples = validator.OneOf([(1,2),(3,4),(5,6)])

    def test_validate_pass(self):
        self.section='pass'
        values = [
            3,
            5,
            7,
            9,
            None,
            ]
        check_pass('function',self, self.fn, values)
        check_pass('class', self, self.class_fn, values)

    def test_validate_fail(self):
        self.section='fail'
        values = [
            'foo',
            ['a','b','c'],
            '1',
            2,
            4,
            6,
            8,
            10,
            '',
            [],
            ]
        check_fail('function', self, self.fn, values)
        check_fail('class', self, self.class_fn, values)

    def test_validate_chars_pass(self):
        self.section='pass'
        values = [
            'y',
            'b',
            'l',
            'n',
            ]
        check_pass('function',self, self.fn_chars, values)
        check_pass('class', self, self.class_fn_chars, values)

    def test_validate_chars_fail(self):
        self.section='fail'
        values = [
            'foo',
            ['a','b','c'],
            '1',
            2,
            4,
            6,
            8,
            10,
            '',
            [],
            'x',
            'yy',
            'yn',
            ]
        check_fail('function', self, self.fn_chars, values)
        check_fail('class', self, self.class_fn_chars, values)

    def test_validate_lists_pass(self):
        self.section='pass'
        values = [
            (1,2),
            (3,4),
            (5,6),
            None,
            ]
        check_pass('function',self, self.fn_list_tuples, values)
        check_pass('class', self, self.class_fn_list_tuples, values)

    def test_validate_lists_fail(self):
        self.section='fail'
        values = [
            'foo',
            ['a','b','c'],
            '1',
            2,
            4,
            6,
            8,
            10,
            '',
            [],
            'x',
            'yy',
            'yn',
            ]
        check_fail('function', self, self.fn_list_tuples, values)
        check_fail('class', self, self.class_fn_list_tuples, values)

    def test_validate_emptyset(self):
        self.section='fail'
        class_fn = validator.OneOf([])
        values = [
            (1,2),
            (3,4),
            (5,6),
            ]
        check_fail('class',self,class_fn, values)



class TestLength(unittest.TestCase):

    type = 'Length'

    fn_min = staticmethod( lambda v: validate.has_length(v, min=3) )
    class_fn_min = validator.Length(min=3)

    fn_max = staticmethod( lambda v: validate.has_length(v, max=3) )
    class_fn_max = validator.Length(max=3)

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
        except error.Invalid, e:
            assert 'more' in e.message
        try:
            self.fn_max('aaaaaaaaaa')
        except error.Invalid, e:
            assert 'fewer' in e.message

    def test_noattrs(self):
        try:
            validate.has_length(1)
        except:
            self.fail('unexpected error using no attrs for validate.has_length')
            

class TestRange(unittest.TestCase):

    type = 'Range'

    fn_min = staticmethod( lambda v: validate.is_in_range(v, min=3) )
    class_fn_min = validator.Range(min=3)

    fn_max = staticmethod( lambda v: validate.is_in_range(v, max=3) )
    class_fn_max = validator.Range(max=3)

    fn_between = staticmethod( lambda v: validate.is_in_range(v, min=1,max=3) )
    class_fn_between = validator.Range(min=1,max=3)

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
        except error.Invalid, e:
            assert 'greater' in e.message
        try:
            self.fn_max(999999)
        except error.Invalid, e:
            assert 'less' in e.message
        try:
            self.fn_between(-999999)
        except error.Invalid, e:
            assert 'between' in e.message
        
    def test_noattrs(self):
        try:
            validate.is_in_range(1)
            return
        except:
            pass
        self.fail('unexpected error using no attrs for validate.is_in_range')

class TestAll_StringRequired(unittest.TestCase):

    type='All'
    fn = validator.All(validator.String(), validator.Required())

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

    def test_messages(self):
        try:
            self.fn(None)
        except error.Invalid, e:
            self.assertEquals(len(e.errors),1)
            self.assertEquals('is required',e.errors[0])
        try:
            self.fn(1)
        except error.Invalid, e:
            self.assertEquals(len(e.errors),1)
            self.assertEquals('must be a string',e.errors[0])


class TestAny_IntegerString(unittest.TestCase):

    type='Any'
    fn = validator.Any(validator.String(), validator.Integer())

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

    def test_messages(self):
        try:
            self.fn(datetime.now())
        except error.Invalid, e:
            self.assertEquals(len(e.errors),2)
            assert 'string' in ''.join(e.errors)
            assert 'integer' in ''.join(e.errors)


class TestAny_RangeInteger(unittest.TestCase):

    type='AnyRangeInteger'
    fn = validator.Any(validator.Range(min=8), validator.Integer())

    def test_validate_pass(self):
        self.section='pass'
        values = [
            4,
            12.3,
            15,
            None,
            ]
        check_pass('class', self, self.fn, values)

    def test_validate_fail(self):
        self.section='fail'
        values = [
            3.4,
        ]
        check_fail('class', self, self.fn, values)


class Test_RequiredAndIntegerOrString(unittest.TestCase):

    type='RequiredAndIntegerOrString'
    fn = validator.All(
            validator.Required(),
            validator.Any(
                validator.String(), 
                validator.Integer()
            )
        )

    def test_validate_pass(self):
        self.section='pass'
        values = [
            '1',
            1,
            1L,
            ]
        check_pass('class', self, self.fn, values)

    def test_validate_fail(self):
        self.section='fail'
        values = [
            0.5,
            datetime.now(),
            None,
        ]
        check_fail('class', self, self.fn, values)

    def test_messages(self):
        try:
            self.fn(datetime.now())
        except error.Invalid, e:
            self.assertEquals(len(e.errors),2)
            assert 'string' in ''.join(e.errors)
            assert 'integer' in ''.join(e.errors)

class TestAlways(unittest.TestCase):

    type='Always'
    class_fn = validator.Always()

    def test_validate_pass(self):
        self.section='pass'
        values = [
            'foo',
            '1',
            u'foobar',
            'sad',
            None,
            1,
            datetime.now(),
            '',
            [],
            -1,
            ]
        check_pass('class', self, self.class_fn, values)
        if validator.Always():
            self.fail("Always should have non-zero")


class TestValidationIncludes(unittest.TestCase):

    def test_no_validator(self):
        """
        Check hunting amongst nothing always fails.
        """
        assert not util.validation_includes(None, validator.Required)
        assert not util.validation_includes(None, validator.Email)

    def test_with_functions(self):
        """
        Check hunting doesn't explode with plain old functions.
        """
        def f(v):
            pass
        assert not util.validation_includes(f, validator.Required)
        assert not util.validation_includes(validator.All(f, f), validator.Required)
        assert util.validation_includes(validator.All(f, validator.Required()), validator.Required)
        assert not util.validation_includes(validator.Any(f, validator.Required()), validator.Required)

    def test_immediate(self):
        """
        Check that the hunt succeeds when the searched for validator is exactly
        the same type.
        """
        assert util.validation_includes(validator.Required(), validator.Required)
        assert not util.validation_includes(validator.Required(), validator.Email)

    def test_inside_all(self):
        """
        Check when inside an All.
        """
        assert util.validation_includes(validator.All(validator.Required()), validator.Required)
        assert not util.validation_includes(validator.All(validator.Required()), validator.Email)

    def test_inside_any_with_others(self):
        """
        Check when inside an Any with other types.
        """
        assert not util.validation_includes(validator.Any(validator.Required(), validator.Email()), validator.Required)
        assert not util.validation_includes(validator.Any(validator.Required(), validator.Email()), validator.Email)

    def test_inside_any_on_own(self):
        """
        Check inside an Any, on own.
        """
        assert util.validation_includes(validator.Any(validator.Required()), validator.Required)
        assert not util.validation_includes(validator.Any(validator.Required()), validator.Email)

    def test_inside_any_only_type(self):
        """
        Check inside an Any, amongst validators of same type.
        """
        assert util.validation_includes(validator.Any(validator.Required(), validator.Required()), validator.Required)
        assert not util.validation_includes(validator.Any(validator.Required(), validator.Required()), validator.Email)


# XXX check that functions can be used for validation

