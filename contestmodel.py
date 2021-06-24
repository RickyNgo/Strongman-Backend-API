from bson import ObjectId
from pydantic import Field
from pydantic.main import BaseModel
from pyobjectid import PyObjectId


class ContestModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    contest_id: str = Field(...)
    name: str = Field(...)
    number: str = Field(...)
    most_recent: str = Field(...)
    type: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
