from fastapi.responses import JSONResponse

def success(data):
    return JSONResponse(status_code=200, content={"data": data})

def error(message, details=None, code=500):
    return JSONResponse(status_code=code, content={
        "error": message,
        "details": details
    })
