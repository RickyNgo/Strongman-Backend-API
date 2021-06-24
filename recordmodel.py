from bson import ObjectId
from pydantic import Field
from pydantic.main import BaseModel
from pyobjectid import PyObjectId


class RecordModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    record_id: str = Field(...)
    record: str = Field(...)
    athlete: str = Field(...)
    country: str = Field(...)
    value: str = Field(...)
    contests: str = Field(...)
    type: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
