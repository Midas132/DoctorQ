import datetime
import enum

from pydantic import BaseModel, Field


class Gender(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

    def polish(self) -> str:
        match self:
            case Gender.MALE:
                return "M"
            case Gender.FEMALE:
                return "K"
            case Gender.OTHER:
                return "I"


class Patient(BaseModel):
    first_name: str
    last_name: str
    pesel: str = Field(..., pattern="^\\d{11}$")
    age: int = Field(..., gt=0)
    gender: Gender
    appointment_time: datetime.datetime = Field(default_factory=datetime.datetime.now)
