import dialogflow
import json
import os
import pymongo
import uuid

mongo_client = pymongo.MongoClient(
    "mongodb+srv://{}:{}@{}".format(
        os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWORD"), os.getenv("MONGO_URL")
    )
)
db = mongo_client.motivdb


def get_daily(request):
    try:

        request_json = request.get_json(silent=True)
        user_id = request_json["user_id"]

        task_list = db.objects.find({"user_id": user_id})

        list_message = []

        for task in task_list:
            verb = task["param_verb"]
            obj = task["param_object"]
            quantifier = task["param_quantifier"]
            abstain = task["param_abstain"]
            historic = task["historic"]
            streak = task["streak"]

            if len(abstain) > 0:
                list_message.append(
                    "You have not {} {} for {} days. Nice job.".format(
                        verb, obj, streak
                    )
                )
            else:
                if len(historic) > 0:
                    average = 0
                    for value, unit in historic:
                        average += value / len(historic)
                    list_message.append(
                        "You have {} {} on average {} {} on the last days. Congrats.".format(
                            verb, obj, average, unit
                        )
                    )
                else:
                    list_message.append(
                        "You have {} {} for {} days. You did it.".format(
                            verb, obj, streak
                        )
                    )

        answer = {"message": list_message}
        return json.dumps(answer)
    except:
        print("BYE WORLD")
        return '{"message": "Error"}'
