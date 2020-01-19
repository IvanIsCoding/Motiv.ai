import json
import pymongo


def get_daily(request):
    try:
        answer = {
            "message": [
                "You have been learning a language for 364 days, congrats",
                "You washed the dishes today",
                "You drank 300ml on average this week",
                "You have walked less than yesterday. Try finding a walking buddy",
            ]
        }
        return json.dumps(answer)
    except:
        print("BYE WORLD")
        return '{"message": "Error"}'
