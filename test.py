try:
    validate.Any(
        validate.Integer(), 
        validate.All(
            validate.Length(max=5),
            validate.String()
        )
    ).validate('213123213')
except Exception, e:
    print list(e.list_errors())
