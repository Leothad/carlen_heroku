from pydantic import BaseModel, Field
from bson.objectid import ObjectId as BsonObjectId


class ObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise ValueError("Not a valid ObjectId")
        return str(v)


class Car(BaseModel):
    id: ObjectId = Field(None, alias='_id')
    car: str = None
    brand: str = None
    model: str = None
    link: str = None
    overview: list = None
    technical_specification: list = None
    safety: list = None
    security: list = None

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data


class Prediction(BaseModel):
    id: ObjectId = Field(None, alias='_id')
    prediction: str = None
    confidence: float = None
    accuracy: float = None
    fn: str = None

    def to_bson(self):
        data = self.dict(by_alias=True, exclude_none=True)
        if data.get("_id") is None:
            data.pop("_id", None)
        return data
