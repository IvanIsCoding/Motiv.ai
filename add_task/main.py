def add_task(request):
    try:
    	request_json = request.get_json(silent=True)
    	print("HELLO WORLD: {}".format(request_json))
    	return "Task has been added!\n"
    except:
    	print("BYE WORLD")
    	return "Error"