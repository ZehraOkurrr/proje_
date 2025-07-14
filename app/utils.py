from app.schemas import ResponseModel

def success_response(data):
    return {"status": True, "data": data}

def error_response(message):
    return {"status": False, "message": message}
