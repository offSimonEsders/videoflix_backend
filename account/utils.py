from rest_framework.utils import json


def get_data(request):
    try:
        return json.loads(request.body)
    except:
        request_data = request.data
        return json.loads(json.dumps(request_data.dict()))