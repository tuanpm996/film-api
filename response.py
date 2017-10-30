import json

def status_ok(object={}):
    object['success'] = True
    return json.dumps(object), 200, {'ContentType': 'application/json'}
