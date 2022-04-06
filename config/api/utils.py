def get_request(context):
    try:
        request = context.get('request')
        print(context, '--' * 100)
    except KeyError:
        raise KeyError({
            'error': 'request was not received'
        })
    return request
