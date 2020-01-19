import json
import pymongo


def add_task(request):
    try:
        request_json = request.get_json(silent=True)
        print("HELLO WORLD: {}".format(request_json))
        answer = {"debug": request_json, "message": "Task has been added"}
        return json.dumps(answer)
    except:
        print("BYE WORLD")
        return '{"message": "Error"}'
