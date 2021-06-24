from bson import ObjectId
from pydantic import Field
from pydantic.main import BaseModel
from pyobjectid import PyObjectId


class ResultModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    result_id: str = Field(...)
    date: str = Field(...)
    contest: str = Field(...)
    contest_type: str = Field(...)
    location: str = Field(...)
    champion: str = Field(...)
    type = type

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
