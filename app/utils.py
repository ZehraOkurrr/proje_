from fastapi.responses import JSONResponse
from typing import Any, Type
from pydantic import BaseModel

def deep_clean(d):
    if isinstance(d, dict):
        return {k: deep_clean(v) for k, v in d.items() if v is not None}
    elif isinstance(d, list):
        return [deep_clean(i) for i in d if i is not None]
    else:
        return d

def serialize(data: Any, schema: Type[BaseModel]):
    if isinstance(data, list):
        return [schema.model_validate(obj).model_dump() for obj in data]
    return schema.model_validate(data).model_dump()

class CustomJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        cleaned = deep_clean(content)
        return super().render(cleaned)

def success_response(data: Any, schema: Type[BaseModel]) -> CustomJSONResponse:
    return CustomJSONResponse(content={
        "status": True,
        "data": serialize(data, schema)
    })

def error_response(message: str) -> CustomJSONResponse:
    return CustomJSONResponse(content={
        "status": False,
        "message": message
    })
