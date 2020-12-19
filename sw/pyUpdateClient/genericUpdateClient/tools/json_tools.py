import json


def json_from_any(any):
    js = json.dumps(any_dict(any), indent=4, sort_keys=True, default=str)
    return js


def any_dict(any):
    myDict = None

    if type(any) is dict:
        myDict = any
    else:
        has_dict = getattr(any, "__dict__", None)
        if has_dict:
            myDict = any.__dict__

    if myDict is None:
        myDict = any

    return myDict