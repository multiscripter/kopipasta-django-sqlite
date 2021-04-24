def validate(params):
    errors = {}
    for name in ['category_id', 'current_id']:
        if name in params:
            if not params[name].isdigit():
                errors[name] = 'Not a number'
            elif int(params[name]) < 1:
                errors[name] = 'Less than one'

    if 'action' in params \
            and params['action'] not in ['first', 'last', 'prev', 'next']:
        errors['action'] = 'Unknown action'

    return errors
