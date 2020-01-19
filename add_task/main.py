import json
import os
import pymongo
import uuid

client = pymongo.MongoClient(
    "mongodb+srv://{}:{}@{}".format(
        os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWORD"), os.getenv("MONGO_URL")
    )
)
db = client.motivdb


def add_task(request):
    try:
        request_json = request.get_json(silent=True)
        task_id = str(uuid.uuid4())
        db.objects.insert_one(
            {
                "user_id": "1111",
                "task_id": task_id,
            }
        )
        answer = {
            "debug": request_json,
            "message": "Task has been added",
            "task_id": task_id,
        }
        print("HELLO WORLD: {}".format(json.dumps(answer)))
        return json.dumps(answer)
    except:
        print("BYE WORLD")
        return '{"message": "Error"}'
