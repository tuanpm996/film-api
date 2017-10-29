import json

def status_ok(object):
    # Reference safe guard.
    if object is None:
        object = {}

    object['success'] = True
    return json.dumps(object), 200, {'ContentType': 'application/json'}
