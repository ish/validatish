
About Validatish
================

Validatish is a validating library, initially built to support the Formish forms library.

How does Validatish work?
+++++++++++++++++++++++++

Validatish is split into two main section, validate and validator. Validate is a set of functions that raise exceptions on failure and validator is a class wrapper around the validate library that also adds composite validators.

The Validate Module
+++++++++++++++++++

Validate implements the following validators.. 


.. autofunction:: validatish.validate.is_required
.. autofunction:: validatish.validate.is_string
.. autofunction:: validatish.validate.is_plaintext
.. autofunction:: validatish.validate.is_integer
.. autofunction:: validatish.validate.is_number
.. autofunction:: validatish.validate.is_email
.. autofunction:: validatish.validate.is_url
.. autofunction:: validatish.validate.is_equal
.. autofunction:: validatish.validate.is_one_of
.. autofunction:: validatish.validate.has_length
.. autofunction:: validatish.validate.is_in_range

The Validate Module
+++++++++++++++++++

Validators implements the following validator classes

.. autoclass:: validatish.validator.Required
.. autoclass:: validatish.validator.String
.. autoclass:: validatish.validator.PlainText
.. autoclass:: validatish.validator.Email
.. autoclass:: validatish.validator.URL
.. autoclass:: validatish.validator.Integer
.. autoclass:: validatish.validator.Number
.. autoclass:: validatish.validator.Equal
.. autoclass:: validatish.validator.OneOf
.. autoclass:: validatish.validator.Length
.. autoclass:: validatish.validator.Range
.. autoclass:: validatish.validator.Any
.. autoclass:: validatish.validator.All
.. autoclass:: validatish.validator.Always


