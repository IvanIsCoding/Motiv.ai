import dialogflow
import json
import os
import pymongo
import random
import uuid

mongo_client = pymongo.MongoClient(
    "mongodb+srv://{}:{}@{}".format(
        os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWORD"), os.getenv("MONGO_URL")
    )
)
db = mongo_client.motivdb

DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
DIALOGFLOW_LANGUAGE_CODE = os.getenv("DIALOGFLOW_LANGUAGE_CODE")
SESSION_ID = str(uuid.uuid4())

dialog_client = dialogflow.SessionsClient()
dialog_session = dialog_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)


def update_task(request):
    try:

        request_json = request.get_json(silent=True)

        text_to_be_analyzed = request_json["contents"]
        user_id = request_json["user_id"]
        task_id = str(uuid.uuid4())

        text_input = dialogflow.types.TextInput(
            text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE
        )

        query_input = dialogflow.types.QueryInput(text=text_input)
        dialog_response = dialog_client.detect_intent(
            session=dialog_session, query_input=query_input
        )

        dialog_params = dict(dialog_response.query_result.parameters.items())
        param_concat = lambda x, y: ("param_" + x, y)

        dialog_params = dict(
            [param_concat(param, val) for param, val in dialog_params.items()]
        )

        task_filter = {
            "param_verb": dialog_params["param_verb"],
            "param_object": dialog_params["param_object"],
            "user_id": user_id,
        }

        task_update = {"$inc": {"streak": 1}}

        param_unit = dialog_params["param_unit"]
        param_quantity = dialog_params["param_quantity"]

        if param_quantity != "":
            task_update["$push"] = {"historic": [param_quantity, param_unit]}

        task_count = db.objects.count(task_filter)

        db.objects.update_one(task_filter, task_update)

        positive_messages = [
            "Nice job.",
            "Congratulations.",
            "You're killing it.",
            "Every marathon begins with one step, nice.",
            "You're rocking it.",
        ]

        answer_message = "I did not find a goal for that. Maybe you should add it!"

        if task_count > 0:
            answer_message = positive_messages[
                random.randint(0, len(positive_messages))
            ]

        answer = {
            "debug": request_json,
            "message": answer_message,
            "task_id": task_id,
            "dialog": dialog_params,
        }

        return json.dumps(answer)

    except:
        return '{"message": "Error"}'
