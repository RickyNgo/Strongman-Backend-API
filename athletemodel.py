from bson import ObjectId
from pydantic import Field
from pydantic.main import BaseModel
from pyobjectid import PyObjectId


class AthleteModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    athlete_id: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    country: str = Field(...)
    active: str = Field(...)
    intl_contests: str = Field(...)
    intl_wins: str = Field(...)
    wsms: str = Field(...)
    wsm_finals: str = Field(...)
    wsm_wins: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
