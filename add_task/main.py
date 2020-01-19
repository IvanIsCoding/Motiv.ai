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

DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
DIALOGFLOW_LANGUAGE_CODE = os.getenv("DIALOGFLOW_LANGUAGE_CODE")
SESSION_ID = str(uuid.uuid4())

dialog_client = dialogflow.SessionsClient()
dialog_session = dialog_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)


def add_task(request):
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

        db.objects.insert_one(
            {
                "user_id": user_id,
                "task_id": task_id,
                "params": dialog_params,
                "streak": 0,
            }
        )

        answer = {
            "debug": request_json,
            "message": dialog_response.query_result.fulfillment_text,
            "task_id": task_id,
            "dialog": dialog_params,
        }

        return json.dumps(answer)

    except:
        return '{"message": "Error"}'
