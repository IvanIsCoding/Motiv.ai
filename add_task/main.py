import json
import os
import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://{}:{}@{}".format(
        os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWORD"), os.getenv("MONGO_URL")
    )
)
db = client.motivdb


def add_task(request):
    try:
        request_json = request.get_json(silent=True)
        print("HELLO WORLD: {}".format(request_json))
        answer = {
            "debug": request_json,
            "message": "Task has been added",
            "mongoUser": os.getenv("MONGO_USER"),
        }
        return json.dumps(answer)
    except:
        print("BYE WORLD")
        return '{"message": "Error"}'
